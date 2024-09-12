import imageio.v3 as iio

chicks = ['chicklet1.png', 'chicklet2.png']
chick_gif = [ ]

for chick in chicks:
  chick_gif.append(iio.imread(chick))

iio.imwrite('chick_gif.gif', chick_gif, duration = 500, loop = 0)

# cd \Onedrive\Skrivebord\codex_kode
