# Maintainer: Michal Krenek (Mikos) <m.krenek@gmail.com>
pkgname=python-signaller
_pkgname=signaller
pkgver=1.1.0
pkgrel=1
pkgdesc="Signals and slots implementation with asyncio support"
arch=('any')
url="https://github.com/xmikos/signaller"
license=('MIT')
depends=('python')
makedepends=('python-setuptools')
source=(https://github.com/xmikos/signaller/archive/v$pkgver.tar.gz)

build() {
  cd "$srcdir/${_pkgname}-$pkgver"
  python setup.py build
}

package() {
  cd "$srcdir/${_pkgname}-$pkgver"
  python setup.py install --root="$pkgdir"
}

# vim:set ts=2 sw=2 et:
