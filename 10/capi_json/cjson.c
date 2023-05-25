#include <stdlib.h>
#include <stdio.h>
// #include <string.h>

#include <Python.h>


PyObject* strvalue_to_number(char* value_str){
    char *stopstring;
    PyObject *value = NULL;

    int val = strtol(value_str, &stopstring, 10);
    if(stopstring[0] == '\0'){
        if (!(value = Py_BuildValue("i", val))) {
            printf("ERROR: Failed to build integer value\n");
            return NULL;
        }
    } else{
        double val = strtod(value_str, &stopstring);
        if (stopstring[0] == '\0'){
            if (!(value = Py_BuildValue("d", val))) {
                printf("ERROR: Failed to build double value\n");
                return NULL;
            }
        } else {
            PyErr_Format(PyExc_TypeError, "Expected object or value");
            return NULL;
        }
    }
    return value;
}


PyObject* strvalue_to_obj(size_t value_start, size_t value_end, const char* string){
    char *value_str;
    PyObject *value = NULL;

    if(value_end - value_start < 1){
        return NULL;
    }
    else if (value_end - value_start == 1){
        value_str = strndup(string + value_start, value_end - value_start);
        value = strvalue_to_number(value_str);
    } else if (string[value_start] == '"' && string[value_end - 1] == '"'){
        value_str = strndup(string + value_start + 1, value_end - value_start - 2);
        if (!(value = Py_BuildValue("s", value_str))) {
            printf("ERROR: Failed to build string value\n");
            return NULL;
        }
    } else {
        value_str = strndup(string + value_start, value_end - value_start);
        value = strvalue_to_number(value_str);
    }
    return value;
}


int handle_item(size_t item_start, size_t item_end, const char* string,
 size_t* key_start, size_t* key_end, size_t* value_start, size_t* value_end){
    while (item_start < item_end && isspace(string[item_start]))
        item_start++;
    while (item_start < item_end && isspace(string[item_end - 1]))
        item_end--;

    if (item_start >= item_end)
        return 0;

    if (string[item_start] != '"'){
        return 0;
    }

    size_t i = item_start, raw_key_start = item_start;
    while (string[i] != ':' && i < item_end)
        i++;


    if(i >= item_end){
        return 0;
    }

    size_t raw_key_end = i;
    while (raw_key_start < raw_key_end && isspace(string[raw_key_end - 1]))
        raw_key_end--;


    if (raw_key_end - raw_key_start < 2 || string[raw_key_start] != '"' || string[raw_key_end - 1] != '"'){
        return 0;
    }


    *key_start = raw_key_start + 1;
    *key_end = raw_key_end - 1;

    i++;  //cause i -> ':' 
    while (i < item_end && isspace(string[i]))
        i++;

    if (i >= item_end){
        return 0;
    }

    *value_start = i, *value_end = item_end;
    return 1;
}


PyObject* cjson_loads(PyObject* self, PyObject* args){
    const char *string;

    if(!PyArg_ParseTuple(args, "s", &string))
    {
        printf("ERROR: Failed to parse arguments");
        return NULL;
    }

    PyObject *dict;
    if (!(dict = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }

    size_t str_len = strlen(string);

    if (str_len < 2 || string[0] != '{' || string[str_len - 1] != '}'){
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }

    int empty_dict = 1;
    for (size_t i = 1; i < str_len - 1; i++){
        if (!isspace(string[i])){
            empty_dict = 0;
            break;
        }
    }
    if (empty_dict)
        return dict;

    size_t i = 1, item_start = 1;
    size_t key_start, key_end, value_start, value_end;
    int partial_success;
    int in_string = 0;
    for(; i < str_len - 1; i++){
        // printf("in loop\n");
        if (string[i] == '"')
            in_string = 1 - in_string;
        if(string[i] == ',' && !in_string){
            partial_success = handle_item(item_start, i, string, &key_start, &key_end, &value_start, &value_end);
            if(partial_success){
                PyObject *key = NULL;
                PyObject *value = NULL;

                char* key_str = strndup(string + key_start, key_end - key_start);
                if (!(key = Py_BuildValue("s", key_str))) {
                    printf("ERROR: Failed to build string value\n");
                    return NULL;
                }

                value = strvalue_to_obj(value_start, value_end, string);
                if(!value){
                    return NULL;
                }

                if (PyDict_SetItem(dict, key, value) < 0) {
                    printf("ERROR: Failed to set item\n");
                    return NULL;
                }
            } else {
                PyErr_Format(PyExc_TypeError, "Expected object or value");
                return NULL;
            }

            item_start = i + 1;
        }
    }
    partial_success = handle_item(item_start, str_len - 1, string, &key_start, &key_end, &value_start, &value_end);
    if(partial_success){
        PyObject *key = NULL;
        PyObject *value = NULL;

        char* key_str = strndup(string + key_start, key_end - key_start);
        if (!(key = Py_BuildValue("s", key_str))) {
            printf("ERROR: Failed to build string value\n");
            return NULL;
        }

        value = strvalue_to_obj(value_start, value_end, string);
        if(!value){
            return NULL;
        }

        if (PyDict_SetItem(dict, key, value) < 0) {
            printf("ERROR: Failed to set item\n");
            return NULL;
        }
    } else {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }

    return dict;
}


static PyMethodDef methods[] = {
    {"loads", cjson_loads, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL}
};

static PyModuleDef utilsmodule = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    "Module for my first c api code.",
    -1,
    methods
};


PyMODINIT_FUNC PyInit_cjson(void)
{
    return PyModule_Create(&utilsmodule);
}