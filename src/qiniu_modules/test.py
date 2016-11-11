import qiniu
import requests


if __name__ == '__main__':
    ak='7yNbTp0tCH0MbstARiiT8p8wxKYBzpx5Y1suQnU8'
    sk='yuUcaWFtB9B_U-mRzW1i3pLAd0jGaAdIe2Jtova7'
    q = qiniu.Auth(ak,sk)
    a,b,c = qiniu.BucketManager(q).list('oiday','21-12-2015')
    print(c)
