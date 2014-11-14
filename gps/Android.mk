ifeq ($(BOARD_HAS_GPS),true)

LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)

LOCAL_MODULE_PATH := $(TARGET_OUT_SHARED_LIBRARIES)
LOCAL_C_INCLUDES += \
	hardware/nexell/pyrope/include

LOCAL_SRC_FILES := board-gps.cpp
LOCAL_MODULE := libgps-drone
LOCAL_MODULE_TAGS := optional
include $(BUILD_STATIC_LIBRARY)

endif
