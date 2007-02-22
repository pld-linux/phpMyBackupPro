# TODO
# - webapps
Summary:	Web-based MySQL backup program, written in PHP
Summary(pl.UTF-8):	Oparty o PHP program do tworzenia kopii zapasowych baz MySQL
Name:		phpMyBackupPro
Version:	2.0b
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/phpmybackup/%{name}.v.%{version}.zip
# Source0-md5:	bd41ce642bb9181c3f2546b09a0d074a
Source1:	%{name}.conf
Source2:        %{name}_lighttpd.conf
URL:		http://www.phpmybackuppro.net/
BuildRequires:	unzip
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	webserver
Requires:	webserver(php)
Requires:       webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_mybackupdir	%{_datadir}/%{name}
%define		_webapps		/etc/webapps
%define		_webapp			%{name}
%define		_sysconfdir		%{_webapps}/%{_webapp}

%description
phpMyBackupPro is a web-based MySQL backup program, written in PHP.
You can schedule backups, email or upload them using FTP and backup
your data or structure or both. It comes with an easy to use
interface, an easy install and config and an online help.

%description -l pl.UTF-8
phpMyBackupPro to oparty o PHP program do tworzenia kopii zapasowych
baz MySQL. Posiada wiele możliwości takich jak: kolejkowanie,
wysyłanie za pomocą e-maila lub FTP, archiwizacja danych zawartych w
bazie, struktury bazy lub obydwu. Wyposażony został w bardzo
przejrzysty i łatwy w użyciu interfejs oraz intuicyjną instalację i
konfigurację programu.

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mybackupdir} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd}

cp -af %{name}/* $RPM_BUILD_ROOT%{_mybackupdir}
rm -f $RPM_BUILD_ROOT%{_mybackupdir}/config.php $RPM_BUILD_ROOT%{_mybackupdir}/global_conf.php

install %{name}/global_conf.php %{name}/config.php $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_mybackupdir}/config.php
ln -sf %{_sysconfdir}/global_conf.php $RPM_BUILD_ROOT%{_mybackupdir}/global_conf.php

install %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}.conf
install %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%triggerpostun -- %{name} < 6.5-2.1
# nuke very-old config location (this mostly for Ra)
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/httpd.conf
fi

# migrate from apache-config macros
if [ -f /etc/%{name}/apache.conf.rpmsave ]; then
	if [ -d /etc/httpd/webapps.d ]; then
		cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
		cp -f /etc/%{name}/apache.conf.rpmsave %{_sysconfdir}/httpd.conf
	fi
	rm -f /etc/%{name}/apache.conf.rpmsave
fi

rm -f /etc/httpd/httpd.conf/99_%{name}.conf
/usr/sbin/webapp register httpd %{_webapp}
%service -q httpd reload

%files
%defattr(644,root,root,755)
%doc documentation/{GNU\ GPL.txt,INSTALL.txt,HISTORY.txt,SEVERAL_SERVERS.txt,SHELL_MODE.txt,UPGRADE.txt}
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%dir %{_mybackupdir}
%{_mybackupdir}/export
%{_mybackupdir}/language
%{_mybackupdir}/*.php
%{_mybackupdir}/stylesheets
%{_mybackupdir}/javascripts.js
%dir %{_mybackupdir}/images
%{_mybackupdir}/images/*.gif
%{_mybackupdir}/images/logo.png
