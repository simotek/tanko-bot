#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    m_pUi(new Ui::MainWindow),
    m_pClient(new WebsocketClient(QUrl(QStringLiteral("ws://172.16.1.61:8702")), true))
    // m_pClient(new WebsocketClient(QUrl(QStringLiteral("ws://192.168.69.242:8702")), true))
{
    m_pUi->setupUi(this);

    QFont f = font();
    f.setBold(true);

    m_pUi->speedDisplay->setFont(f);
    // connect(client, &WebsocketClient::LeftSpeed, ui->leftSlider, &QSlider::setValue);
    // connect(client, &WebsocketClient::RightSpeed, ui->rightSlider, &QSlider::setValue);

    connect(m_pUi->forwardButton, &QPushButton::pressed, m_pClient, &WebsocketClient::forward);
    connect(m_pUi->forwardButton, &QPushButton::released, m_pClient, &WebsocketClient::stop);

    connect(m_pUi->reverseButton, &QPushButton::pressed, m_pClient, &WebsocketClient::reverse);
    connect(m_pUi->reverseButton, &QPushButton::released, m_pClient, &WebsocketClient::stop);

    connect(m_pUi->leftButton, &QPushButton::pressed, m_pClient, &WebsocketClient::left);
    connect(m_pUi->leftButton, &QPushButton::released, m_pClient, &WebsocketClient::stop);

    connect(m_pUi->rightButton, &QPushButton::pressed, m_pClient, &WebsocketClient::right);
    connect(m_pUi->rightButton, &QPushButton::released, m_pClient, &WebsocketClient::stop);

    connect(m_pUi->stopButton, &QPushButton::pressed, m_pClient, &WebsocketClient::stop);
    connect(m_pUi->stopButton, &QPushButton::released, m_pClient, &WebsocketClient::stop);

    connect(m_pUi->speedDial, SIGNAL(valueChanged(int)), this, SLOT(setSpeed(int)));
    connect(m_pUi->speedlSlider, SIGNAL(valueChanged(int)), this, SLOT(setSpeed(int)));

    setSpeed(80);
}

MainWindow::~MainWindow()
{
    delete m_pUi;
}

void MainWindow::setSpeed(int val)
{
    m_pUi->speedDial->setValue(val);
    m_pUi->speedlSlider->setValue(val);

    m_pUi->speedDisplay->setText(QString::number(val));

    m_pClient->setSpeed(val);
}
