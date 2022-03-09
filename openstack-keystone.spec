%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%global with_doc 1
%global service keystone
# guard for package OSP does not support
%global rhosp 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Keystone is a Python implementation of the OpenStack \
(http://www.openstack.org) identity service API.

Name:           openstack-keystone
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:          1
Version:        XXX
Release:        XXX
Summary:        OpenStack Identity Service
License:        ASL 2.0
URL:            http://keystone.openstack.org/
Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
Source1:        openstack-keystone.logrotate
Source3:        openstack-keystone.sysctl
Source5:        openstack-keystone-sample-data
Source20:       keystone-dist.conf
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:  openstack-macros
BuildRequires:  python3-devel
BuildRequires:  python3-osprofiler >= 1.1.0
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  git-core
# Required to build keystone.conf
BuildRequires:  python3-oslo-cache >= 1.26.0
BuildRequires:  python3-oslo-config >= 2:6.8.0
BuildRequires:  python3-passlib >= 1.6
BuildRequires:  python3-pycadf >= 2.1.0
# Required to compile translation files
BuildRequires:  python3-babel
# Required to build man pages
BuildRequires:  python3-oslo-policy
BuildRequires:  python3-jsonschema >= 2.6.0
BuildRequires:  python3-oslo-db >= 4.27.0
BuildRequires:  python3-oauthlib
BuildRequires:  python3-pysaml2
BuildRequires:  python3-keystonemiddleware >= 7.0.0
BuildRequires:  python3-testresources
BuildRequires:  python3-testscenarios
BuildRequires:  python3-oslotest
BuildRequires:  python3-redis
%if 0%{rhosp} == 0 && 0%{?rhel} < 8
BuildRequires:  python3-zmq
%endif
BuildRequires:  python3-ldappool >= 2.0.0
BuildRequires:  python3-webtest
BuildRequires:  python3-freezegun

Requires:       python3-keystone = %{epoch}:%{version}-%{release}
Requires:       python3-keystoneclient >= 1:3.8.0

%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
BuildRequires: systemd
Requires(pre):    shadow-utils

%description
%{common_desc}

This package contains the Keystone daemon.

%package -n       python3-keystone
Summary:          Keystone Python libraries
%{?python_provide:%python_provide python3-keystone}

Requires:       python3-pbr >= 2.0.0
Requires:       python3-bcrypt >= 3.1.3
Requires:       python3-sqlalchemy >= 1.3.0
Requires:       python3-passlib >= 1.7.0
Requires:       openssl
Requires:       python3-oauthlib >= 0.6.2
Requires:       python3-jsonschema >= 3.2.0
Requires:       python3-pycadf >= 1.1.0
Requires:       python3-keystonemiddleware >= 7.0.0
Requires:       python3-oslo-cache >= 1.26.0
Requires:       python3-oslo-config >= 2:6.8.0
Requires:       python3-oslo-context >= 2.22.0
Requires:       python3-oslo-db >= 6.0.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.44.0
Requires:       python3-oslo-messaging >= 5.29.0
Requires:       python3-oslo-middleware >= 3.31.0
Requires:       python3-oslo-policy >= 3.10.0
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-oslo-upgradecheck >= 1.3.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-osprofiler >= 1.4.0
Requires:       python3-pysaml2 >= 5.0.0
Requires:       python3-stevedore >= 1.20.0
Requires:       python3-scrypt >= 0.8.0
Requires:       python3-flask >= 1:1.0.2
Requires:       python3-flask-restful >= 0.3.5
Requires:       python3-jwt >= 1.6.1
Requires:       python3-pytz >= 2013.6
# for Keystone Lightweight Tokens (KLWT)
Requires:       python3-cryptography >= 2.7
Requires:       python3-ldap >= 3.1.0
Requires:       python3-ldappool >= 2.0.0
Requires:       python3-memcached >= 1.56
Requires:       python3-migrate >= 0.13.0
Requires:       python3-webob >= 1.7.1
Requires:       python3-dogpile-cache >= 1.0.2
Requires:       python3-msgpack >= 0.5.0


%description -n   python3-keystone
%{common_desc}

This package contains the Keystone Python library.

%package -n python3-%{service}-tests
Summary:        Keystone tests
%{?python_provide:%python_provide python3-%{service}-tests}
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

# Adding python-keystone-tests-tempest as Requires to keep backward
# compatibilty

%description -n python3-%{service}-tests
%{common_desc}

This package contains the Keystone test files.


%if 0%{?with_doc}
%package doc
Summary:        Documentation for OpenStack Identity Service

# for API autodoc
BuildRequires:  python3-sphinx >= 1.1.2
BuildRequires:  python3-sphinx-feature-classification
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinxcontrib-apidoc
BuildRequires:  python3-sphinxcontrib-seqdiag
BuildRequires:  python3-sphinxcontrib-blockdiag
BuildRequires:  python3-flask >= 1:1.0.2
BuildRequires:  python3-flask-restful >= 0.3.5
BuildRequires:  python3-cryptography >= 2.1
BuildRequires:  python3-oslo-log >= 3.44.0
BuildRequires:  python3-oslo-messaging >= 5.29.0
BuildRequires:  python3-oslo-middleware >= 3.31.0
BuildRequires:  python3-oslo-policy >= 2.3.0
BuildRequires:  python3-mock
BuildRequires:  python3-dogpile-cache >= 0.5.7
BuildRequires:  python3-memcached >= 1.56
BuildRequires:  python3-lxml


%description doc
%{common_desc}

This package contains documentation for Keystone.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n keystone-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;
# Let RPM handle the dependencies
%py_req_cleanup

# adjust paths to WSGI scripts
sed -i 's#/local/bin#/bin#' httpd/wsgi-keystone.conf
sed -i 's#apache2#httpd#' httpd/wsgi-keystone.conf

%build
PYTHONPATH=. oslo-config-generator --config-file=config-generator/keystone.conf
PYTHONPATH=. oslo-config-generator --config-file=config-generator/keystone.conf --format yaml --output-file=%{service}-schema.yaml
PYTHONPATH=. oslo-config-generator --config-file=config-generator/keystone.conf --format json --output-file=%{service}-schema.json
# distribution defaults are located in keystone-dist.conf

%{py3_build}
# Generate i18n files
%{__python3} setup.py compile_catalog -d build/lib/%{service}/locale -D keystone

%install
%{py3_install}

# Keystone doesn't ship policy.json file but only an example
# that contains data which might be problematic to use by default.
# Instead, ship an empty file that operators can override.
echo "{}" > policy.json

install -d -m 755 %{buildroot}%{_sysconfdir}/keystone
install -d -m 755 %{buildroot}%{_sysconfdir}/keystone/policy.d
install -p -D -m 640 etc/keystone.conf.sample %{buildroot}%{_sysconfdir}/keystone/keystone.conf
install -p -D -m 640 policy.json %{buildroot}%{_sysconfdir}/keystone/policy.json
install -p -D -m 640 %{service}-schema.yaml %{buildroot}%{_datadir}/%{service}/%{service}-schema.yaml
install -p -D -m 640 %{service}-schema.json %{buildroot}%{_datadir}/%{service}/%{service}-schema.json
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_datadir}/keystone/keystone-dist.conf
install -p -D -m 640 etc/logging.conf.sample %{buildroot}%{_sysconfdir}/keystone/logging.conf
install -p -D -m 640 etc/default_catalog.templates %{buildroot}%{_sysconfdir}/keystone/default_catalog.templates
install -p -D -m 640 etc/sso_callback_template.html %{buildroot}%{_sysconfdir}/keystone/sso_callback_template.html
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-keystone
install -d -m 755 %{buildroot}%{_prefix}/lib/sysctl.d
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_prefix}/lib/sysctl.d/openstack-keystone.conf
# Install sample data script.
install -p -D -m 755 tools/sample_data.sh %{buildroot}%{_datadir}/keystone/sample_data.sh
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_bindir}/openstack-keystone-sample-data
# Install sample HTTPD integration files
install -p -D -m 644 httpd/wsgi-keystone.conf  %{buildroot}%{_datadir}/keystone/

install -d -m 755 %{buildroot}%{_sharedstatedir}/keystone
install -d -m 755 %{buildroot}%{_localstatedir}/log/keystone

# cleanup config files installed by keystone
# we already generate them w/ oslo-config-generator
rm -rf %{buildroot}/%{_prefix}%{_sysconfdir}

# docs generation requires everything to be installed first
%if 0%{?with_doc}
sphinx-build -b html doc/source doc/build/html

# https://storyboard.openstack.org/#!/story/2005577
mkdir -p doc/build/man/_static
sphinx-build -b man doc/source doc/build/man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif
%if 0%{?with_doc}
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python3_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

%pre
# 163:163 for keystone (openstack-keystone) - rhbz#752842
getent group keystone >/dev/null || groupadd -r --gid 163 keystone
getent passwd keystone >/dev/null || \
useradd --uid 163 -r -g keystone -d %{_sharedstatedir}/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemons" keystone
exit 0

%post
%sysctl_apply openstack-keystone.conf
# Install keystone.log file before, so both keystone & root users can write in it.
touch %{_localstatedir}/log/keystone/keystone.log
chown root:keystone %{_localstatedir}/log/keystone/keystone.log
chmod 660 %{_localstatedir}/log/keystone/keystone.log

%files
%license LICENSE
%doc README.rst
%if 0%{?with_doc}
%{_mandir}/man1/keystone*.1.gz
%endif
%{_bindir}/keystone-wsgi-admin
%{_bindir}/keystone-wsgi-public
%{_bindir}/keystone-manage
%{_bindir}/keystone-status
%{_bindir}/openstack-keystone-sample-data
%dir %{_datadir}/keystone
%attr(0644, root, keystone) %{_datadir}/keystone/keystone-dist.conf
%attr(0644, root, keystone) %{_datadir}/keystone/%{service}-schema.yaml
%attr(0644, root, keystone) %{_datadir}/keystone/%{service}-schema.json
%attr(0755, root, root) %{_datadir}/keystone/sample_data.sh
%attr(0644, root, keystone) %{_datadir}/keystone/wsgi-keystone.conf
%dir %attr(0750, root, keystone) %{_sysconfdir}/keystone
%dir %attr(0750, root, keystone) %{_sysconfdir}/keystone/policy.d
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/logging.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/policy.json
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/default_catalog.templates
%config(noreplace) %attr(0640, keystone, keystone) %{_sysconfdir}/keystone/sso_callback_template.html
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-keystone
%dir %attr(-, keystone, keystone) %{_sharedstatedir}/keystone
%dir %attr(0750, keystone, keystone) %{_localstatedir}/log/keystone
%ghost %attr(0660, root, keystone) %{_localstatedir}/log/keystone/keystone.log
%{_prefix}/lib/sysctl.d/openstack-keystone.conf


%files -n python3-keystone -f %{service}.lang
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/keystone
%{python3_sitelib}/keystone-*.egg-info
%exclude %{python3_sitelib}/%{service}/tests

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
