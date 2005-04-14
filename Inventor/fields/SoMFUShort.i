%{
static void
convert_SoMFUShort_array(PyObject *input, int len, unsigned short *temp)
{
  int i;

  for (i=0; i<len; i++) {
    PyObject *oi = PySequence_GetItem(input,i);
    if (PyNumber_Check(oi)) {
      temp[i] = (unsigned short) PyInt_AsLong(oi);
    } else {
      PyErr_SetString(PyExc_ValueError,"Sequence elements must be numbers");
      free(temp);       
      return;
    }
  }
  return;
}
%}

%typemap(in) short * (short *temp) {
  int len;

  if (PySequence_Check($input)) {
    len = PySequence_Length($input);
    temp = (unsigned short *) malloc(len*sizeof(unsigned short));
    convert_SoMFUShort_array($input, len, temp);
  
    $1 = temp;
  } else {
    PyErr_SetString(PyExc_TypeError, "expected a sequence.");
  }
}

%ignore SoMFUShort::getValues(const int start) const;

%typemap(in,numinputs=1) (int & len, int i) {
   $1 = new int;
   *$1 = 0;
   $2 = PyInt_AsLong($input);
}

%typemap(argout) (int & len, int i) {
  Py_XDECREF($result);   /* Blow away any previous result */
  $result = PyList_New(*$1);
  if(result) {
    for(int i = 0; i < *$1; i++){ PyList_SetItem($result, i, PyInt_FromLong((long)result[i])); }
  }
  delete $1;
}

%feature("shadow") SoMFUShort::setValues %{
def setValues(*args):
   if len(args) == 2:
      if isinstance(args[1], SoMFUShort):
         val = args[1].getValues()
         return _pivy.SoMFUShort_setValues(args[0],0,len(val),val)
      else:
         return _pivy.SoMFUShort_setValues(args[0],0,len(args[1]),args[1])
   elif len(args) == 3:
      if isinstance(args[2], SoMFUShort):
         val = args[2].getValues()
         return _pivy.SoMFUShort_setValues(args[0],args[1],len(val),val)
      else:
         return _pivy.SoMFUShort_setValues(args[0],args[1],len(args[2]),args[2])
   return _pivy.SoMFUShort_setValues(*args)
%}

%extend SoMFUShort {
  const unsigned short __getitem__(int i) {
    return (*self)[i];
  }
  void  __setitem__(int i, unsigned short value) {
    self->set1Value(i, value);
  }
  const unsigned short * __getValuesHelper__(int & len, int i) {
    if( i < 0 || i > self->getNum())
      return 0;
    len = self->getNum() - i;
    return self->getValues(i);
  }
/* implement getValues to have default argument etc. */
%pythoncode %{
   def getValues(*args):
     if len(args) == 1:
        return _pivy.SoMFUShort___getValuesHelper__(args[0], 0)
     return _pivy.SoMFUShort___getValuesHelper__(*args)
%}
}
