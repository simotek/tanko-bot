#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "WebsocketClient.hpp"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    WebsocketClient * client = new WebsocketClient(QUrl(QStringLiteral("ws://10.0.0.2:8702")), true);

    // connect(client, &WebsocketClient::LeftSpeed, ui->leftSlider, &QSlider::setValue);
    // connect(client, &WebsocketClient::RightSpeed, ui->rightSlider, &QSlider::setValue);

    connect(ui->forwardButton, &QPushButton::pressed, client, &WebsocketClient::forward);
    connect(ui->forwardButton, &QPushButton::released, client, &WebsocketClient::stop);

    connect(ui->reverseButton, &QPushButton::pressed, client, &WebsocketClient::reverse);
    connect(ui->reverseButton, &QPushButton::released, client, &WebsocketClient::stop);

    connect(ui->leftButton, &QPushButton::pressed, client, &WebsocketClient::left);
    connect(ui->leftButton, &QPushButton::released, client, &WebsocketClient::stop);

    connect(ui->rightButton, &QPushButton::pressed, client, &WebsocketClient::right);
    connect(ui->rightButton, &QPushButton::released, client, &WebsocketClient::stop);


}

MainWindow::~MainWindow()
{
    delete ui;
}
