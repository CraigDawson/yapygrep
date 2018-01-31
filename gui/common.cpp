#include "common.h"
#include "ui_common.h"

Common::Common(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::Common)
{
    ui->setupUi(this);
}

Common::~Common()
{
    delete ui;
}
