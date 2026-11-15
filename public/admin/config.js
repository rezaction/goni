/* Dashboard (Decap CMS) configuration. Edit REPO below once, to your GitHub "owner/repository". */
(function () {
  var REPO = 'YOUR-GITHUB-USER/gonest-website';   // <-- change this
  var BRANCH = 'main';

  var str = function (name, label, extra) { return Object.assign({ name: name, label: label, widget: 'string' }, extra || {}); };
  var text = function (name, label, extra) { return Object.assign({ name: name, label: label, widget: 'text' }, extra || {}); };
  var strList = function (name, label) { return { name: name, label: label, widget: 'list', field: { name: 'item', label: 'Item', widget: 'string' } }; };
  var slugPattern = ['^[a-z0-9]+(-[a-z0-9]+)*$', 'Lowercase letters, numbers and hyphens only (for example: my-new-article)'];

  var photoRef = { name: 'photo', label: 'Photo slot', widget: 'relation', collection: 'photos', file: 'photos',
    search_fields: ['slots.*.key', 'slots.*.label_en'], value_field: 'slots.*.key', display_fields: ['slots.*.label_en'],
    hint: 'Pick a photo from the Photos collection. Add the photo there first.' };
  var categoryRef = function () { return { name: 'category', label: 'Category', widget: 'relation', collection: 'categories',
    search_fields: ['en.name'], value_field: 'slug_en', display_fields: ['en.name'] }; };

  var catLang = function (code, label) {
    return { name: code, label: label, widget: 'object', fields: [
      str('name', 'Name'), str('short', 'Short name'), text('desc', 'Card description'),
      str('moq', 'Minimum order (shown on cards)'), str('formats', 'Formats'),
      str('hero', 'Page heading'), text('lead', 'Page intro'),
      strList('intro', 'Intro paragraphs'), strList('types', 'Product types'), strList('formula', 'Formula options'), strList('pack', 'Packaging options'),
      { name: 'specs', label: 'Key numbers (MOQ, lead time, price)', widget: 'list', fields: [str('label', 'Label'), str('value', 'Value')] },
      { name: 'faqs', label: 'FAQ', widget: 'list', fields: [str('q', 'Question'), text('a', 'Answer')] }
    ] };
  };
  var projLang = function (code, label) {
    return { name: code, label: label, widget: 'object', fields: [
      str('name', 'Project name'), str('client', 'Client'), str('note', 'One-line summary'),
      str('fmt', 'Format'), str('batch', 'First batch'), str('time', 'Time to launch'),
      text('need', 'Client need'), text('concept', 'Concept'), text('challenge', 'Challenge'), text('solution', 'Solution'), text('result', 'Result')
    ] };
  };
  var artLang = function (code, label) {
    return { name: code, label: label, widget: 'object', fields: [
      str('category', 'Category'), str('read', 'Reading time (for example: 6 min read)'),
      str('title', 'Title'), text('description', 'Summary (also used for Google)'),
      { name: 'sections', label: 'Sections', widget: 'list', fields: [str('heading', 'Heading'), strList('paragraphs', 'Paragraphs (a few short lines show as a bullet list)')] },
      { name: 'related', label: 'Related links', widget: 'list', required: false, fields: [str('path', 'Page path (for example: /products/coffee/)'), str('label', 'Link text')] }
    ] };
  };
  var prodLang = function (code, label) {
    return { name: code, label: label, widget: 'object', fields: [
      str('name', 'Product'), str('format', 'Format'), str('moq', 'Minimum order'), str('price', 'Indicative price'), str('lead_time', 'Lead time')
    ] };
  };
  var testiLang = function (code, label) {
    return { name: code, label: label, widget: 'object', fields: [text('quote', 'Quote'), str('name', 'Name'), str('role', 'Role and company')] };
  };

  window.GONEST_CMS_CONFIG = {
    load_config_file: false,
    backend: { name: 'github', repo: REPO, branch: BRANCH, base_url: window.location.origin, auth_endpoint: 'oauth/auth' },
    site_url: window.location.origin,
    media_folder: 'uploads',
    public_folder: '/uploads',
    locale: 'en',
    collections: [
      { name: 'settings', label: 'Settings', files: [{ name: 'settings', label: 'General settings', file: 'content/settings.json', format: 'json', fields: [
        str('brand', 'Brand name', { hint: 'Display only. Text inside pages says GoNEST; to rename the brand, ask your developer.' }),
        str('domain', 'Website address', { hint: 'For example https://www.yourdomain.com. Used in Google tags and the sitemap.' }),
        str('whatsapp', 'WhatsApp number (links)', { hint: 'International format, digits only, for example 6281234567890', pattern: ['^[0-9]{8,16}$', 'Digits only, no + or spaces'] }),
        str('whatsapp_display', 'WhatsApp number (as shown)'),
        str('email', 'Email address'),
        { name: 'hours', label: 'Office hours', widget: 'object', fields: [str('en', 'English'), str('id', 'Indonesian')] },
        { name: 'address', label: 'Address', widget: 'object', fields: [str('en', 'English'), str('id', 'Indonesian')] },
        { name: 'stats', label: 'Home page numbers', widget: 'list', min: 1, max: 4, fields: [
          str('en_value', 'Value (English)'), str('en_label', 'Label (English)'), str('id_value', 'Value (Indonesian)'), str('id_label', 'Label (Indonesian)')] },
        { name: 'analytics', label: 'Analytics', widget: 'object', fields: [
          str('ga_id', 'Google Analytics ID', { required: false, hint: 'G-XXXXXXXXXX. Empty = analytics off' }),
          str('clarity_id', 'Microsoft Clarity ID', { required: false })] },
        { name: 'demo', label: 'Demo mode', widget: 'object', fields: [
          { name: 'enabled', label: 'Show the demo marquee and hide the site from Google', widget: 'boolean', default: true },
          str('tape_text', 'Marquee text')] }
      ] }] },
      { name: 'categories', label: 'Product categories', label_singular: 'Category', folder: 'content/categories', extension: 'json', format: 'json',
        create: true, delete: true, identifier_field: 'slug_en', slug: '{{fields.slug_en}}', summary: '{{order}}. {{en.name}}',
        fields: [
          str('slug_en', 'English URL name', { pattern: slugPattern, hint: 'Part of the address, for example coffee. Do not change after publishing.' }),
          str('slug_id', 'Indonesian URL name', { pattern: slugPattern }),
          { name: 'order', label: 'Order on the site', widget: 'number', value_type: 'int', min: 1, default: 10 },
          photoRef, catLang('en', 'English'), catLang('id', 'Indonesian')] },
      { name: 'products', label: 'Products and prices', label_singular: 'Product', folder: 'content/products', extension: 'json', format: 'json',
        create: true, delete: true, identifier_field: 'slug', slug: '{{fields.slug}}', summary: '{{en.name}} ({{category}})',
        fields: [
          str('slug', 'File name', { pattern: slugPattern, hint: 'Lowercase, hyphens only. Not shown to visitors.' }),
          { name: 'order', label: 'Order in the price table', widget: 'number', value_type: 'int', min: 1, default: 10 },
          categoryRef(), prodLang('en', 'English'), prodLang('id', 'Indonesian')] },
      { name: 'projects', label: 'Portfolio projects', label_singular: 'Project', folder: 'content/projects', extension: 'json', format: 'json',
        create: true, delete: true, identifier_field: 'slug', slug: '{{fields.slug}}', summary: '{{en.name}}',
        fields: [
          str('slug', 'URL name (same in English and Indonesian)', { pattern: slugPattern }),
          { name: 'date', label: 'Date', widget: 'datetime', date_format: 'YYYY-MM-DD', time_format: false, format: 'YYYY-MM-DD' },
          categoryRef(), photoRef, projLang('en', 'English'), projLang('id', 'Indonesian')] },
      { name: 'articles', label: 'Insights articles', label_singular: 'Article', folder: 'content/articles', extension: 'json', format: 'json',
        create: true, delete: true, identifier_field: 'slug_en', slug: '{{fields.slug_en}}', summary: '{{en.title}}',
        fields: [
          str('slug_en', 'English URL name', { pattern: slugPattern, hint: 'Part of the address. Do not change after publishing.' }),
          str('slug_id', 'Indonesian URL name', { pattern: slugPattern }),
          { name: 'date', label: 'Date', widget: 'datetime', date_format: 'YYYY-MM-DD', time_format: false, format: 'YYYY-MM-DD' },
          { name: 'order', label: 'Order when dates are equal', widget: 'number', value_type: 'int', min: 1, default: 50 },
          artLang('en', 'English'), artLang('id', 'Indonesian')] },
      { name: 'testimonials', label: 'Testimonials', label_singular: 'Testimonial', folder: 'content/testimonials', extension: 'json', format: 'json',
        create: true, delete: true, identifier_field: 'slug', slug: '{{fields.slug}}', summary: '{{en.name}}',
        fields: [
          str('slug', 'File name', { pattern: slugPattern }),
          { name: 'order', label: 'Order', widget: 'number', value_type: 'int', min: 1, default: 10 },
          testiLang('en', 'English'), testiLang('id', 'Indonesian')] },
      { name: 'photos', label: 'Photos', files: [{ name: 'photos', label: 'Photo slots', file: 'content/photos.json', format: 'json', fields: [
        { name: 'slots', label: 'Photos', widget: 'list', summary: '{{fields.label_en}}', fields: [
          str('key', 'Slot key', { hint: 'Identifier used by pages. Do not rename an existing one.' }),
          str('label_en', 'Name (English)'), str('label_id', 'Name (Indonesian)'),
          { name: 'image', label: 'Photo', widget: 'image', required: false,
            hint: 'Upload any JPG, PNG or WebP of any size. It is compressed to WebP and cropped to the 3:2 slot automatically when the site updates.',
            media_library: { config: { multiple: false } } }] }] }] }
    ]
  };
})();
