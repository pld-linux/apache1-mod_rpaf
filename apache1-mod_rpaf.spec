# TODO
# - compile fails when apache1 is compiled with ipv6
%define		mod_name	rpaf
%define 	apxs		%{_sbindir}/apxs1
Summary:	Apache module: record traffic statistics into a database
Summary(pl):	Modu� Apache'a: zapisywanie statystyk ruchu do bazy danych
Name:		apache1-mod_%{mod_name}
Version:	0.5
Release:	0.13
License:	Apache
Group:		Networking/Daemons
Source0:	http://stderr.net/apache/rpaf/download/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	471fb059d6223a394f319b7c8ab45c4d
Source1:	%{name}.conf
URL:		http://stderr.net/apache/rpaf/
BuildRequires:	apache1-devel >= 1.3.33-2
BuildConflicts:	apache1(ipv6)-devel
Requires:	apache1 >= 1.3.33-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
rpaf is for backend Apache servers what mod_proxy_add_forward is for
frontend Apache servers. It does excactly the opposite of
mod_proxy_add_forward written by Ask Bj�rn Hansen. It will also work
with mod_proxy in Apache starting with release 1.3.25.

%description -l pl
rpaf jest dla backendowych serwer�w Apache tym, czym
mod_proxy_add_forward jest dla frontendowych. Wykonuje dok�adnie
przeciwne operacje do mod_proxy_add_forward napisanego przez Aska
Bjorna Hansena. B�dzie tak�e dzia�a� z mod_proxy w Apache'u pocz�wszy
od wersji 1.3.25.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/99_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES test.pl
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
