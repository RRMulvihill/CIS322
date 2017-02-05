curl http://download.nextag.com/apache//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2
tar -xjf httpd-2.4.25.tar.bz2 
cd httpd-2.4.25
./configure --prefix=$1
make
make install
git clone https://github.com/postgres/postgres.git
cd postgres
./configure --prefix=$1
make
make install
