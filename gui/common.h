#ifndef COMMON_H
#define COMMON_H

#include <QDialog>

namespace Ui {
class Common;
}

class Common : public QDialog
{
    Q_OBJECT

public:
    explicit Common(QWidget *parent = 0);
    ~Common();

private:
    Ui::Common *ui;
};

#endif // COMMON_H
