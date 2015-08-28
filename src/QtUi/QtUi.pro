#-------------------------------------------------
#
# Project created by QtCreator 2015-08-27T19:26:55
#
#-------------------------------------------------

QT       += core gui websockets

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

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
    ../build-QtUi-Android_for_armeabi_v7a_GCC_4_9_Qt_5_5_0-Debug/android-build/AndroidManifest.xml \
    ../build-QtUi-Android_for_armeabi_v7a_GCC_4_9_Qt_5_5_0-Debug/android-build/bin/AndroidManifest.xml

