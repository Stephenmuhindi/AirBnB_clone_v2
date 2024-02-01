# Puppet Manifest that configures a server in 
# readiness for deployment
package { 'nginx':
  ensure   => 'present',
  provider => 'apt',
} 

file { '/data':
  ensure  => 'directory',
  require => Package['nginx']
} 

file { '/data/web_static':
  ensure  => 'directory',
  require => File['/data']
} -> file { '/data/web_static/releases':
  ensure => 'directory',
} -> file { '/data/web_static/releases/test':
  ensure => 'directory',
} -> file { '/data/web_static/shared':
  ensure => 'directory',
} -> file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => "Holberton School Puppet\n",
} -> file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
} -> exec { 'chown -R ubuntu:ubuntu /data/':
  path => '/usr/bin/:/usr/local/bin/:/bin/',
} -> file { '/var/www':
  ensure => 'directory',
} -> file { '/var/www/html':
  ensure => 'directory',
} -> file { '/var/www/html/index.html':
  ensure  => 'present',
  content => "Holberton School Nginx\n",
} -> file { '/var/www/html/404.html':
  ensure  => 'present',
  content => "Ceci n'est pas une page\n",
} -> file_line { 'add_hbnb_static_location':
  path    => '/etc/nginx/sites-enabled/default',
  line    => '        location /hbnb_static {',
  match   => '#server_name _;',
  after   => '#a',
  content => '            alias /data/web_static/current/;',
} -> exec { 'nginx restart':
  command => 'sudo /etc/init.d/nginx restart',
  path    => '/etc/init.d/',
}
