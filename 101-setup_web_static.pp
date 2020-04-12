# Setups a new web server for deployment

file { '/data':
  ensure => 'directory',
  path   => '/data',
  owner  => 'ubuntu',
  group  => 'ubuntu'
}

file { '/data/web_static':
  ensure  => 'directory',
  path    => '/data/web_static',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data']
}

file { '/data/web_static/releases':
  ensure  => 'directory',
  path    => '/data/web_static/releases',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static']
}

file { '/data/web_static/releases/test':
  ensure  => 'directory',
  path    => '/data/web_static/releases/test',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases']
}

file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  path    => '/data/web_static/releases/test/index.html',
  content => 'Test index.html',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static/releases/test']
}

file { '/data/web_static/shared':
  ensure  => 'directory',
  path    => '/data/web_static/shared',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static']
}

file { '/data/web_static/current':
  ensure  => 'link',
  target  => '/data/web_static/releases/test',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  require => File['/data/web_static', '/data/web_static/releases/test']
}

exec { 'apt-get update':
  path    => '/usr/bin',
  require => File['/data/web_static/current']
}

package { 'nginx':
  ensure  => 'installed',
  require => Exec['apt-get update']
}

exec { 'retrieve_cfg':
  command => 'wget https://raw.githubusercontent.com/stephenchu530/AirBnB_clone_v2/master/default -O /etc/nginx/sites-available/default',
  path    => '/usr/bin',
  require => Package['nginx']
}

file { '/etc/nginx/sites-available/default':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => 644,
  require => Exec['retrieve_cfg']
}

service { 'nginx':
  ensure  => 'running',
  require => File['/etc/nginx/sites-available/default']
}
