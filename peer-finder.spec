# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

Name: peer-finder
Epoch: 100
Version: 1.1.0
Release: 1%{?dist}
Summary: Peer finder daemon for StatefulSet
License: Apache-2.0
URL: https://github.com/kmodules/peer-finder/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: golang-1.19
BuildRequires: glibc-static

%description
This is a simple peer finder daemon that is useful with StatefulSet and
related use cases. All it does is watch DNS for changes in the set of
endpoints that are part of the governing service of the PetSet. It
periodically looks up the SRV record of the DNS entry that corresponds
to a Kubernetes Service which enumerates the set of peers for this the
specified service.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
mkdir -p bin
set -ex && \
    export CGO_ENABLED=0 && \
    go build \
        -mod vendor -buildmode pie -v \
        -ldflags "-s -w -extldflags '-static -lm'" \
        -o ./bin/peer-finder .

%install
install -Dpm755 -d %{buildroot}%{_bindir}
install -Dpm755 -t %{buildroot}%{_bindir}/ bin/peer-finder

%files
%license LICENSE
%{_bindir}/*

%changelog
