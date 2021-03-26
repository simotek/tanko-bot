#-------------------------------------------------
#
# Project created by QtCreator 2015-08-27T19:26:55
#
#-------------------------------------------------

QT       += core gui widgets websockets

TARGET = QtUi
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    WebsocketClient.cpp

HEADERS  += mainwindow.h \
    WebsocketClient.hpp

FORMS    += mainwindow.ui

CONFIG += mobility
MOBILITY = 

RESOURCES += \
    images.qrc

DISTFILES += \
    android/AndroidManifest.xml \
    android/Makefile \
    android/Makefile \
    android/Makefile \
    android/android-templates-deployment-settings.json \
    android/build.gradle \
    android/gradle.properties \
    android/gradle/wrapper/gradle-wrapper.jar \
    android/gradle/wrapper/gradle-wrapper.properties \
    android/gradlew \
    android/gradlew.bat \
    android/libdummy.prl \
    android/res/values/libs.xml \
    android/templates

ANDROID_PACKAGE_SOURCE_DIR = $$PWD/android

