/****************************************************************************
**
** Copyright (C) 2014 Kurt Pattyn <pattyn.kurt@gmail.com>.
** Contact: http://www.qt.io/licensing/
**
** This file is part of the QtWebSockets module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:LGPL21$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see http://www.qt.io/terms-conditions. For further
** information use the contact form at http://www.qt.io/contact-us.
**
** GNU Lesser General Public License Usage
** Alternatively, this file may be used under the terms of the GNU Lesser
** General Public License version 2.1 or version 3 as published by the Free
** Software Foundation and appearing in the file LICENSE.LGPLv21 and
** LICENSE.LGPLv3 included in the packaging of this file. Please review the
** following information to ensure the GNU Lesser General Public License
** requirements will be met: https://www.gnu.org/licenses/lgpl.html and
** http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
**
** As a special exception, The Qt Company gives you certain additional
** rights. These rights are described in The Qt Company LGPL Exception
** version 1.1, included in the file LGPL_EXCEPTION.txt in this package.
**
** $QT_END_LICENSE$
**
****************************************************************************/
#include "WebsocketClient.hpp"
#include <QtCore/QDebug>

QT_USE_NAMESPACE

WebsocketClient::WebsocketClient(const QUrl &url, bool debug, QObject *parent) :
    QObject(parent),
    m_url(url),
    m_debug(debug)
{



    if (m_debug)
        qDebug() << "WebSocket server:" << url;
    connect(&m_webSocket, &QWebSocket::connected, this, &WebsocketClient::onConnected);
    connect(&m_webSocket, &QWebSocket::disconnected, this, &WebsocketClient::closed);

    connect(&m_webSocket, SIGNAL(QAbstractSocket::SocketError), this, SLOT(onError(QAbstractSocket::SocketError)));

    m_webSocket.open(QUrl(url));

    onError((QAbstractSocket::SocketError)0);
}

void WebsocketClient::onConnected()
{
    if (m_debug)
        qDebug() << "WebSocket connected";

    connect(&m_webSocket, &QWebSocket::textMessageReceived,
            this, &WebsocketClient::onTextMessageReceived);
    connect(&m_webSocket, &QWebSocket::textFrameReceived,
            this, &WebsocketClient::onTextFrameReceived);
    m_webSocket.sendTextMessage(QStringLiteral("Hello, world!"));
}

void WebsocketClient::onTextFrameReceived(QString message)
{
    qDebug() << "Message received:" << message;
}

void WebsocketClient::onTextMessageReceived(QString message)
{
    qDebug() << "Message received:" << message;

    QStringList MsgArgs = message.split(':');

    if (MsgArgs[0] == "DMLS")
    {
        if (MsgArgs.size() > 1)
        {
            emit LeftSpeed(MsgArgs[1].toInt());
        }
    }
    else if (MsgArgs[0] == "DMRS")
    {
        if (MsgArgs.size() > 1)
        {
            emit RightSpeed(MsgArgs[1].toInt());
        }
    }
}

void WebsocketClient::forward()
{
    m_webSocket.sendTextMessage(QStringLiteral("DMC:80,80"));
}

void WebsocketClient::reverse()
{
    m_webSocket.sendTextMessage(QStringLiteral("DMC:-80,-80"));
}

void WebsocketClient::left()
{
    m_webSocket.sendTextMessage(QStringLiteral("DMC:-80,80"));
}

void WebsocketClient::right()
{
    m_webSocket.sendTextMessage(QStringLiteral("DMC:80,-80"));
}

void WebsocketClient::stop()
{
    m_webSocket.sendTextMessage(QStringLiteral("DMC:0,0"));
}

void WebsocketClient::onError(QAbstractSocket::SocketError error)
{
    qDebug("Error: %d %s", error, m_webSocket.errorString().toUtf8().data());
}
