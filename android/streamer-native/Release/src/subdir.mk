################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
/home/djp/projects/ob/android/streamer/jni/streamer/src/AMRAudioFileDescriptorSource.cpp \
/home/djp/projects/ob/android/streamer/jni/streamer/src/streamer.cpp 

OBJS += \
./src/AMRAudioFileDescriptorSource.o \
./src/streamer.o 

CPP_DEPS += \
./src/AMRAudioFileDescriptorSource.d \
./src/streamer.d 


# Each subdirectory must supply rules for building sources it contributes
src/AMRAudioFileDescriptorSource.o: /home/djp/projects/ob/android/streamer/jni/streamer/src/AMRAudioFileDescriptorSource.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	/opt/android-ndk-1.6_r1/build/prebuilt/linux-x86/arm-eabi-4.2.1/arm-eabi/bin/g++ -I"/home/djp/projects/ob/android/streamer/jni/streamer/jni-include" -I"/home/djp/projects/ob/android/streamer/jni/streamer/include" -I"/home/djp/projects/ob/android/streamer/jni/basicusageenvironment/include" -I"/home/djp/projects/ob/android/streamer/jni/groupsock/include" -I"/home/djp/projects/ob/android/streamer/jni/live555/include" -I"/home/djp/projects/ob/android/streamer/jni/usageenvironment/include" -I"/home/djp/projects/ob/android/streamer/jni/include/jnix" -I/opt/android-ndk-1.6_r1/build/platforms/android-3/arch-arm/usr/include -O3 -Wall -c -fmessage-length=0 -fPIC -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

src/streamer.o: /home/djp/projects/ob/android/streamer/jni/streamer/src/streamer.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	/opt/android-ndk-1.6_r1/build/prebuilt/linux-x86/arm-eabi-4.2.1/arm-eabi/bin/g++ -I"/home/djp/projects/ob/android/streamer/jni/streamer/jni-include" -I"/home/djp/projects/ob/android/streamer/jni/streamer/include" -I"/home/djp/projects/ob/android/streamer/jni/basicusageenvironment/include" -I"/home/djp/projects/ob/android/streamer/jni/groupsock/include" -I"/home/djp/projects/ob/android/streamer/jni/live555/include" -I"/home/djp/projects/ob/android/streamer/jni/usageenvironment/include" -I"/home/djp/projects/ob/android/streamer/jni/include/jnix" -I/opt/android-ndk-1.6_r1/build/platforms/android-3/arch-arm/usr/include -O3 -Wall -c -fmessage-length=0 -fPIC -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o"$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


