Summary:	Web-based MySQL backup program, written in PHP
Summary(pl):	Oparty o PHP program do tworzenia kopi zapasowych baz MySQL
Name:		phpMyBackupPro
Version:	1.0
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/phpmybackup/%{name}.v.%{version}.zip
# Source0-md5:	28f9c7465cf8da627a29dcb97c3eeeef
URL:		http://sourceforge.net/projects/phpmybackup/
Requires:	php-mysql
Requires:	php-pcre
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_mybackupdir	/home/services/httpd/html/mybackup

%description
phpMyBackupPro is a web-based MySQL backup program, written in PHP.
You can schedule backups, email or upload them using FTP and backup
your data or structure or both. It comes with an easy to use
interface, an easy install and config and an online help..

%description -l pl
phpMyBackupPro to oparty o PHP program do tworzenia kopii zapasowych
baz MySQL. Posiada wiele mo¿liwo¶ci takich jak: kolejkowanie,
wysy³anie za pomoc± e-maila lub FTP, archiwizacja danych zawartych w
bazie, struktury bazy lub obydwu. Wyposa¿ony zosta³ w bardzo
przejrzysty i ³atwy w u¿yciu interfejs oraz intuicyjn± instalacjê i
konfiguracjê programu.

%prep
%setup -q -c %{name}.v.%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mybackupdir}

cp -af %{name}.v.%{version}/*	  $RPM_BUILD_ROOT%{_mybackupdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc SHELL_MODE INSTALL
%dir %{_mybackupdir}
%{_mybackupdir}/export/
%{_mybackupdir}/language/
%{_mybackupdir}/*.php
%{_mybackupdir}/style.css
%{_mybackupdir}/javascripts.js
