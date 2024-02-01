# Puppet Manifest that configures a server in 
# readiness for deployment
package { 'nginx':
  ensure  => 'present',
  require => Exec['update_apt_store'],
}

exec { 'update_apt_store':
  command => '/usr/bin/apt-get update',
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
} -> file_line { 'add_hbnb_static_location':
  path    => '/etc/nginx/sites-enabled/default',
  line    => '        location /hbnb_static {',
  match   => '#server_name _;',
  after   => '#a',
  content => '            alias /data/web_static/current/;',
} -> exec { 'restart_nginx':
  command => '/usr/sbin/service nginx restart',
}
