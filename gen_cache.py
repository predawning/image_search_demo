from application import get_images, Category

for c in Category:
    pt = get_images(c.value, '/uploads/679b2482-e909-11e4-8ea8-90b11c0ea83f.jpg') 
    print 'gen cache for c.name'
