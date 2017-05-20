#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "WebsocketClient.hpp"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

public slots:
    void setSpeed(int val);

private:
    Ui::MainWindow *m_pUi;

    WebsocketClient * m_pClient;
};

#endif // MAINWINDOW_H
