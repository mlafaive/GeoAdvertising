<h1 id="top">Geo-Advertising</h1>

<h2>Steps to Run</h2>
<ul>
	<li><a href="#cloning">Clone repo</a></li>
	<li><a href="#installing">Install packages</li>
	<li><a href="#db-setup">Set up database</a></li>
	<li><a href="#running">Run Server</a></li>
<ul>

<h2 id="cloning">Clone Repo</h2>
<p>run `git clone https://github.com/mlafaive/GeoAdvertising.git`</p>

<h2 id="installing">Install Packages</h2>
<p>If necessary, <a href="https://pip.pypa.io/en/stable/installing/" target="_blank">install pip</a></p>
<p>run `pip install -r requirements.txt`</p>

<h2 id="db-setup">Set up Database</h2>
<p><a href="https://dev.mysql.com/doc/refman/5.7/en/installing.html" target="_blank">install mysql</a></p>
<p>log into mysql with `mysql -u root -p` (password: root) and run `CREATE DATABASE geo_adv_db;`</p>
<p>run `mysql -u root -p geo_adv_db < create_tables.sql` (password: root)</p>
<p>run `mysql -u root -p geo_adv_db < load_data.sql` (password: root)</p>

<h2 id="running">Run Server</h2>
<p>run `python app.py` and go to http://localhost:3000/</p>


