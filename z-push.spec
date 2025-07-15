Summary:	An Implementation of the ActiveSync protocol
Name:		z-push
Version:	1.2.1
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://download.berlios.de/z-push/%{name}-%{version}.tar.gz
# Source0-md5:	c0a2d6f7f1bfcf3d73580cede4c6eb6c
Patch0:		%{name}.patch
Patch1:		%{name}-apache_request_headers.patch
URL:		http://z-push.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	php-pear-Mail
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Requires:	webserver(php)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Z-push is an implementation of the ActiveSync protocol, which is used
'over-the-air' for multi platform ActiveSync devices, including
Windows Mobile, Ericsson and Nokia phones. With Z-push any groupware
can be connected and synced with these devices.

%prep
%setup -q -n %{name}
find -name '*.php' -print0 | xargs -0 %{__sed} -i -e 's,\r$,,'
%patch -P0 -p1
%patch -P1 -p1

cat > apache.conf <<'EOF'
Alias /Microsoft-Server-ActiveSync %{_appdir}/index.php
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/Microsoft-Server-ActiveSync" => "%{_appdir}/index.php",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a backend $RPM_BUILD_ROOT%{_appdir}
cp -a include $RPM_BUILD_ROOT%{_appdir}
cp -a state $RPM_BUILD_ROOT%{_appdir}

mv $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}/config.php
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc INSTALL
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%{_appdir}
