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

    if (str_len < 2){
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }

    size_t json_start = 0, json_end = str_len;
    while (json_start < json_end && isspace(string[json_start]))
        json_start++;
    while (json_start < json_end && isspace(string[json_end - 1]))
        json_end--;

    if (json_start >= json_end || string[json_start] != '{' || string[json_end - 1] != '}'){
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }

    int empty_dict = 1;
    for (size_t i = json_start + 1; i < json_end - 1; i++){
        if (!isspace(string[i])){
            empty_dict = 0;
            break;
        }
    }
    if (empty_dict)
        return dict;

    size_t i = json_start + 1, item_start = json_start + 1;
    size_t key_start, key_end, value_start, value_end;
    int partial_success;
    int in_string = 0;
    for(; i < json_end - 1; i++){
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
    partial_success = handle_item(item_start, json_end - 1, string, &key_start, &key_end, &value_start, &value_end);
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



PyObject* cjson_dumps(PyObject* self, PyObject* args){
    PyObject *dict;

    if(!PyArg_ParseTuple(args, "O", &dict))
    {
        printf("ERROR: Failed to parse arguments");
        return NULL;
    }

    PyObject *final_string_list = PyList_New(0);
    PyObject *sep = PyUnicode_FromString(": ");
    PyObject *quots = PyUnicode_FromString("\"");
    PyObject *key, *value, *item_str, *value_str;


    Py_ssize_t pos = 0;
    while (PyDict_Next(dict, &pos, &key, &value)){
        if (!PyUnicode_Check(key)){
            PyErr_Format(PyExc_TypeError, "key must be str");
            return NULL;
        }
        PyObject *key_str = PyUnicode_FromObject(key);
        key_str = PyUnicode_Concat(PyUnicode_Concat(PyUnicode_Concat(quots, key), quots), sep);

        if (PyUnicode_Check(value)){
            value_str = PyUnicode_Concat(PyUnicode_Concat(quots, value), quots);
        } else if (PyLong_Check(value)){
            long long val = PyLong_AsLongLong(value);
            int length = snprintf( NULL, 0, "%lld", val );
            char* str = malloc( length + 1 );
            snprintf( str, length + 1, "%lld", val );
            value_str = PyUnicode_FromString(str);
            free(str);
        } else if (PyFloat_Check(value)){
            double val = PyFloat_AsDouble(value);
            int length = snprintf( NULL, 0, "%lf", val );
            char* str = malloc( length + 1 );
            snprintf( str, length + 1, "%g", val );
            value_str = PyUnicode_FromString(str);
            free(str);
        } else{
            PyErr_Format(PyExc_TypeError, "value must be str or number");
            return NULL;
        }
        
        item_str = PyUnicode_Concat(key_str, value_str);
        int status = PyList_Append(final_string_list, item_str);
        // printf("%d", status);
    }
    PyObject *join_sep = PyUnicode_FromString(", ");
    PyObject *final_string = PyUnicode_Join(join_sep, final_string_list);

    PyObject *brl = PyUnicode_FromString("{");
    PyObject *brr = PyUnicode_FromString("}");
    PyObject* string = PyUnicode_Concat(PyUnicode_Concat(brl, final_string), brr);

    return string;
}



static PyMethodDef methods[] = {
    {"loads", cjson_loads, METH_VARARGS, ""},
    {"dumps", cjson_dumps, METH_VARARGS, ""},
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