%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global release_name liberty
%global service keystone
 
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-keystone
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:          1
Version:        8.0.0
Release:        1%{?milestone}%{?dist}
Summary:        OpenStack Identity Service
License:        ASL 2.0
URL:            http://keystone.openstack.org/
Source0:        http://launchpad.net/%{service}/%{release_name}/%{version}/+download/%{service}-%{upstream_version}.tar.gz

Source1:        openstack-keystone.logrotate
Source2:        openstack-keystone.service
Source3:        openstack-keystone.sysctl
Source5:        openstack-keystone-sample-data
Source20:       keystone-dist.conf
Patch0001: 0001-sync-parameter-values-with-keystone-dist.conf.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-pbr >= 1.8
# Required to build keystone.conf
BuildRequires:  python-oslo-config >= 2:2.3.0
BuildRequires:  python-pycadf >= 1.1.0
BuildRequires:  python-redis
BuildRequires:  python-zmq

Requires:       python-keystone = %{epoch}:%{version}-%{release}
Requires:       python-keystoneclient >= 1:1.6.0

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
Requires(pre):    shadow-utils

%description
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone daemon.

%package -n       python-keystone
Summary:          Keystone Python libraries

Requires:       python-pbr
Requires:       python-eventlet
Requires:       python-ldap
Requires:       python-ldappool
Requires:       python-memcached
Requires:       python-migrate >= 0.9.6
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-routes >= 1.12
Requires:       python-sqlalchemy >= 0.9.9
Requires:       python-webob >= 1.2.3
Requires:       python-passlib >= 1.6
Requires:       MySQL-python
Requires:       PyPAM
Requires:       python-iso8601
Requires:       openssl
Requires:       python-netaddr
Requires:       python-six >= 1.9.0
Requires:       python-babel
Requires:       python-oauthlib
Requires:       python-dogpile-cache >= 0.5.4
Requires:       python-jsonschema
Requires:       python-pycadf >= 0.8.0
Requires:       python-posix_ipc
Requires:       python-keystonemiddleware >= 2.0.0
Requires:       python-oslo-concurrency >= 2.3.0
Requires:       python-oslo-config >= 2:2.3.0
Requires:       python-oslo-context >= 0.2.0
Requires:       python-oslo-db >= 2.4.1
Requires:       python-oslo-i18n >= 1.5.0
Requires:       python-oslo-log >= 1.8.0
Requires:       python-oslo-messaging >= 2.5.0
Requires:       python-oslo-middleware >= 2.8.0
Requires:       python-oslo-policy >= 0.5.0
Requires:       python-oslo-serialization >= 1.4.0
Requires:       python-oslo-service >= 0.7.0
Requires:       python-oslo-utils >= 2.0.0
Requires:       python-pysaml2
Requires:       python-stevedore >= 1.5.0
# for Keystone Lightweight Tokens (KLWT)
Requires:       python-cryptography
Requires:       python-msgpack

%description -n   python-keystone
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains the Keystone Python library.

%if 0%{?with_doc}
%package doc
Summary:        Documentation for OpenStack Identity Service

BuildRequires:  python-sphinx >= 1.1.2
BuildRequires:  python-oslo-sphinx >= 2.5.0
# for API autodoc
BuildRequires:  python-cryptography
BuildRequires:  python-dogpile-cache >= 0.5.4
BuildRequires:  python-jsonschema
BuildRequires:  python-keystonemiddleware >= 2.0.0
BuildRequires:  python-ldappool
BuildRequires:  python-memcached
BuildRequires:  python-oauthlib
BuildRequires:  python-oslo-concurrency >= 2.3.0
BuildRequires:  python-oslo-db >= 2.4.1
BuildRequires:  python-oslo-log >= 1.8.0
BuildRequires:  python-oslo-messaging >= 2.5.0
BuildRequires:  python-oslo-middleware >= 2.8.0
BuildRequires:  python-oslo-policy >= 0.5.0
BuildRequires:  python-passlib >= 1.6
BuildRequires:  python-paste-deploy
BuildRequires:  python-pysaml2
BuildRequires:  python-routes

%description doc
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.

This package contains documentation for Keystone.
%endif

%prep
%setup -q -n keystone-%{upstream_version}

%patch0001 -p1

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

# adjust paths to WSGI scripts
sed -i 's#/local/bin#/bin#' httpd/wsgi-keystone.conf

%build
PYTHONPATH=. oslo-config-generator --config-file=config-generator/keystone.conf
# distribution defaults are located in keystone-dist.conf

%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/keystone/tests

install -d -m 755 %{buildroot}%{_sysconfdir}/keystone
install -p -D -m 640 etc/keystone.conf.sample %{buildroot}%{_sysconfdir}/keystone/keystone.conf
install -p -D -m 644 etc/keystone-paste.ini %{buildroot}%{_datadir}/keystone/keystone-dist-paste.ini
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_datadir}/keystone/keystone-dist.conf
install -p -D -m 644 etc/policy.v3cloudsample.json %{buildroot}%{_datadir}/keystone/policy.v3cloudsample.json
install -p -D -m 640 etc/logging.conf.sample %{buildroot}%{_sysconfdir}/keystone/logging.conf
install -p -D -m 640 etc/default_catalog.templates %{buildroot}%{_sysconfdir}/keystone/default_catalog.templates
install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/keystone/policy.json
install -p -D -m 640 etc/sso_callback_template.html %{buildroot}%{_sysconfdir}/keystone/sso_callback_template.html
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-keystone
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-keystone.service
install -d -m 755 %{buildroot}%{_prefix}/lib/sysctl.d
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_prefix}/lib/sysctl.d/openstack-keystone.conf
# Install sample data script.
install -p -D -m 755 tools/sample_data.sh %{buildroot}%{_datadir}/keystone/sample_data.sh
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_bindir}/openstack-keystone-sample-data
# Install sample HTTPD integration files
install -p -D -m 644 httpd/keystone.py  %{buildroot}%{_datadir}/keystone/keystone.wsgi
install -p -D -m 644 httpd/wsgi-keystone.conf  %{buildroot}%{_datadir}/keystone/

install -d -m 755 %{buildroot}%{_sharedstatedir}/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/log/keystone

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"
pushd doc
make html
make man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 build/man/*.1 %{buildroot}%{_mandir}/man1/
popd
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%pre
# 163:163 for keystone (openstack-keystone) - rhbz#752842
getent group keystone >/dev/null || groupadd -r --gid 163 keystone
getent passwd keystone >/dev/null || \
useradd --uid 163 -r -g keystone -d %{_sharedstatedir}/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemons" keystone
exit 0

%post
%systemd_post openstack-keystone.service
%sysctl_apply openstack-keystone.conf

%preun
%systemd_preun openstack-keystone.service

%postun
%systemd_postun_with_restart openstack-keystone.service

%files
%license LICENSE
%doc README.rst
%{_mandir}/man1/keystone*.1.gz
%{_bindir}/keystone-all
%{_bindir}/keystone-wsgi-admin
%{_bindir}/keystone-wsgi-public
%{_bindir}/keystone-manage
%{_bindir}/openstack-keystone-sample-data
%dir %{_datadir}/keystone
%attr(0644, root, keystone) %{_datadir}/keystone/keystone-dist.conf
%attr(0644, root, keystone) %{_datadir}/keystone/keystone-dist-paste.ini
%attr(0644, root, keystone) %{_datadir}/keystone/policy.v3cloudsample.json
%attr(0755, root, root) %{_datadir}/keystone/sample_data.sh
%attr(0644, root, keystone) %{_datadir}/keystone/keystone.wsgi
%attr(0644, root, keystone) %{_datadir}/keystone/wsgi-keystone.conf
%{_unitdir}/openstack-keystone.service
%dir %attr(0750, root, keystone) %{_sysconfdir}/keystone
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/logging.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/default_catalog.templates
%config(noreplace) %attr(0640, keystone, keystone) %{_sysconfdir}/keystone/policy.json
%config(noreplace) %attr(0640, keystone, keystone) %{_sysconfdir}/keystone/sso_callback_template.html
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-keystone
%dir %attr(-, keystone, keystone) %{_sharedstatedir}/keystone
%dir %attr(0750, keystone, keystone) %{_localstatedir}/log/keystone
%{_prefix}/lib/sysctl.d/openstack-keystone.conf


%files -n python-keystone
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/keystone
%{python2_sitelib}/keystone-*.egg-info

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Thu Oct 15 2015 Alan Pevec <alan.pevec@redhat.com> 1:8.0.0-1
- Update to upstream 8.0.0

* Tue Oct 06 2015 Alan Pevec <alan.pevec@redhat.com> 1:8.0.0-0.6.0rc2
- Update to upstream 8.0.0.0rc2

* Tue Sep 29 2015 Alan Pevec <alan.pevec@redhat.com> 1:8.0.0-0.5.0rc1
- OpenStack Liberty release candidate

* Thu Sep 17 2015 Alan Pevec <alan.pevec@redhat.com> 1:8.0.0-0.4.0b3
- Update to upstream 8.0.0.0b3

* Tue Aug 04 2015 Alan Pevec <alan.pevec@redhat.com> 1:8.0.0-0.2.0b2
- Update to upstream 8.0.0.0b2

* Fri Jun 19 2015 Alan Pevec <alan.pevec@redhat.com> 2015.1.0-3
- enable federation, pysaml2 is now packaged

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2015.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Alan Pevec <alan.pevec@redhat.com> 2015.1.0-1
- OpenStack Kilo release
