#ifndef JNIX_UTIL_H
#define JNIX_UTIL_H

#include <jni.h>

typedef jobject FileDescriptor;

jboolean setObjectField(JNIEnv *env, jobject obj, const char *fieldName, const char *fieldDescriptor, jobject value);

jboolean getObjectField(JNIEnv *env, jobject obj, const char *fieldName, const char *fieldDescriptor, jobject *out);

jboolean setIntField(JNIEnv *env, jobject obj, const char *fieldName, jint value);

jboolean getIntField(JNIEnv *env, jobject obj, const char *fieldName, jint *out);

void throwException(JNIEnv *env, const char *name, const char *message);

FileDescriptor newFileDescriptor(JNIEnv *env, int descriptor);

jboolean closeFileDescriptor(JNIEnv *env, FileDescriptor fileDescriptor);

#endif
