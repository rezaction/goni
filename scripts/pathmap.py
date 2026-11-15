# English path -> Indonesian path. Shared by build.py and build_id.py.
import content as K
EN_ARTICLE_SLUGS = K.ARTICLE_SLUGS
PROJECT_SLUGS = [x['slug'] for x in K.PROJECTS_EN]

PATHMAP = {
    '/': '/id/',
    '/about/': '/id/tentang-kami/',
    '/about/company-profile/': '/id/tentang-kami/profil-perusahaan/',
    '/about/facilities/': '/id/tentang-kami/fasilitas/',
    '/about/quality-assurance/': '/id/tentang-kami/jaminan-mutu/',
    '/about/certifications/': '/id/tentang-kami/sertifikasi/',
    '/services/': '/id/layanan/',
    '/services/product-development/': '/id/layanan/pengembangan-produk/',
    '/services/contract-manufacturing/': '/id/layanan/jasa-maklon/',
    '/services/private-label/': '/id/layanan/private-label/',
    '/services/oem-odm/': '/id/layanan/oem-odm/',
    '/services/packaging/': '/id/layanan/kemasan/',
    '/products/': '/id/produk/',
    '/how-it-works/': '/id/cara-kerja/',
    '/portfolio/': '/id/portofolio/',
    '/insights/': '/id/wawasan/',
    '/contact/': '/id/kontak/',
    '/privacy-policy/': '/id/kebijakan-privasi/',
    '/terms/': '/id/syarat-ketentuan/',
}
for _c_en, _c_id in zip(K.CATS_EN, K.CATS_ID):
    PATHMAP[f'/products/{_c_en["slug"]}/'] = f'/id/produk/{_c_id["slug"]}/'
for s in PROJECT_SLUGS:
    PATHMAP[f'/portfolio/{s}/'] = f'/id/portofolio/{s}/'
for en, idn in EN_ARTICLE_SLUGS.items():
    PATHMAP[f'/insights/{en}/'] = f'/id/wawasan/{idn}/'
REVERSE = {v: k for k, v in PATHMAP.items()}
