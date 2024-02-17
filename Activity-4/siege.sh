sudo yum install gcc openssl openssl-devel
wget http://download.joedog.org/siege/siege-4.0.4.tar.gz
tar xvfz siege-4.0.4.tar.gz
cd siege-4.0.4
./configure
make
sudo make install


siege -c1000 -d1 -r1 --content-type "application/json" 'https://j9cgl2te7b.execute-api.us-west-2.amazonaws.com/default/act4 POST {"a": "9", "b": "6", "op": "+"}'