# TODO
# - webapps
Summary:	Web-based MySQL backup program, written in PHP
Summary(pl.UTF-8):	Oparty o PHP program do tworzenia kopii zapasowych baz MySQL
Name:		phpMyBackupPro
Version:	1.5
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/phpmybackup/%{name}.v.%{version}.zip
# Source0-md5:	4d2fe3aab2b17d42328aceda9d793dd5
Source1:	%{name}.conf
URL:		http://www.phpmybackuppro.net/
BuildRequires:	unzip
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	webserver
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_mybackupdir	%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

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

cp -af %{name}.v.%{version}/* $RPM_BUILD_ROOT%{_mybackupdir}
rm -f $RPM_BUILD_ROOT%{_mybackupdir}/config.php $RPM_BUILD_ROOT%{_mybackupdir}/global_conf.php

install %{name}.v.%{version}/global_conf.php %{name}.v.%{version}/config.php $RPM_BUILD_ROOT%{_sysconfdir}
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_mybackupdir}/config.php
ln -sf %{_sysconfdir}/global_conf.php $RPM_BUILD_ROOT%{_mybackupdir}/global_conf.php

install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc documentation/{GNU\ GPL.txt,HISTORY.txt,SEVERAL_SERVERS.txt,SHELL_MODE.txt,UPGRADE.txt}
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%config(noreplace) %verify(not md5 mtime size) /etc/httpd/%{name}.conf
%dir %{_mybackupdir}
%{_mybackupdir}/export
%{_mybackupdir}/language
%{_mybackupdir}/*.php
%{_mybackupdir}/stylesheets
%{_mybackupdir}/javascripts.js
%dir %{_mybackupdir}/images
%{_mybackupdir}/images/*.gif
%{_mybackupdir}/images/logo.png
