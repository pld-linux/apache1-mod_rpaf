# TODO
# - compile fails when apache1 is compiled with ipv6
%define		mod_name	rpaf
%define 	apxs		%{_sbindir}/apxs1
Summary:	Apache module: record traffic statistics into a database
Summary(pl):	Modu³ Apache'a: zapisywanie statystyk ruchu do bazy danych
Name:		apache1-mod_%{mod_name}
Version:	0.5
Release:	0.3
License:	Apache
Group:		Networking/Daemons
Source0:	http://stderr.net/apache/rpaf/download/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	471fb059d6223a394f319b7c8ab45c4d
Source1:	%{name}.conf
URL:		http://stderr.net/apache/rpaf/
BuildRequires:	apache1-devel
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires:	apache1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
rpaf is for backend Apache servers what mod_proxy_add_forward is for
frontend Apache servers. It does excactly the opposite of
mod_proxy_add_forward written by Ask Bjørn Hansen. It will also work
with mod_proxy in Apache starting with release 1.3.25.

%description -l pl
rpaf jest dla backendowych serwerów Apache tym, czym
mod_proxy_add_forward jest dla frontendowych. Wykonuje dok³adnie
przeciwne operacje do mod_proxy_add_forward napisanego przez Aska
Bjorna Hansena. Bêdzie tak¿e dzia³aæ z mod_proxy w Apache'u pocz±wszy
od wersji 1.3.25.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /etc/apache/apache.conf ] && ! grep -q "^Include.*mod_%{mod_name}.conf" /etc/apache/apache.conf; then
	echo "Include /etc/apache/mod_%{mod_name}.conf" >> /etc/apache/apache.conf
fi
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	umask 027
	grep -v "^Include.*mod_%{mod_name}.conf" /etc/apache/apache.conf > \
		/etc/apache/apache.conf.tmp
	mv -f /etc/apache/apache.conf.tmp /etc/apache/apache.conf
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES test.pl
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/mod_*.conf
%attr(755,root,root) %{_pkglibdir}/*
