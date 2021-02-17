## Descrição dos dados

**Dataset**: Open Images Dataset V6

Para importar os dados para o banco de dados você precisa:

1. Baixar **todos** os arquivos CSV disponíveis na [página de download](https://storage.googleapis.com/openimages/web/download.html)
   do dataset;
2. Garantir que todos os arquivos CSV estejam no diretório `inspect-open-images/open_images/data`,
   e tenham o mesmo nome e cabeçalho como os outputs de comando `head` abaixo;
3. Rode o comando abaixo para criar o banco de dados da forma como o código Python espera;
4. Para mais instruções sobre os dados e organização do dataset,
   [clique aqui](https://storage.googleapis.com/openimages/web/factsfigures.html);

```
$ cd open_images/data/
$ time rows csv2sqlite oidv6-attributes-description.csv oidv6-class-descriptions-boxable.csv oidv6-train-annotations-bbox.csv train-annotations-human-imagelabels-boxable.csv train-annotations-object-segmentation.csv train-images-boxable-with-rotation.csv db.sqlite3 --samples 30
```

A saída esperada é algo como o log abaixo:

```
[oidv6-attributes-description.csv -> db.sqlite3#oidv6_attributes_description]: 15.0 rows [00:00, 10.5k rows/s]
[oidv6-class-descriptions-boxable.csv -> db.sqlite3#oidv6_class_descriptions_boxable]: 601 rows [00:00, 300k rows/s]
[oidv6-train-annotations-bbox.csv -> db.sqlite3#oidv6_train_annotations_bbox]: 14.6M rows [03:39, 66.7k rows/s]
[train-annotations-human-imagelabels-boxable.csv -> db.sqlite3#train_annotations_human_imagelabels_boxable]: 9.00M rows [00:39, 228k rows/s]
[train-annotations-object-segmentation.csv -> db.sqlite3#train_annotations_object_segmentation]: 2.69M rows [00:29, 92.4k rows/s]
[train-images-boxable-with-rotation.csv -> db.sqlite3#train_images_boxable_with_rotation]: 1.74M rows [00:21, 80.2k rows/s]

real	5m12,243s
user	5m6,008s
sys	0m4,282s
```

### oidv6-attributes-description.csv

```
$ head oidv6-attributes-description.csv
id,name
/m/02gy9n,Transparent
/m/05z87,Plastic
/m/0dnr7,(made of)Textile
/m/04lbp,(made of)Leather

```

### oidv6-class-descriptions-boxable.csv

```
$ head oidv6-class-descriptions-boxable.csv
id,name
/m/011k07,Tortoise
/m/011q46kg,Container
/m/012074,Magpie
```


### oidv6-relationship-triplets.csv

```
$ head oidv6-relationship-triplets.csv
LabelName1,LabelName2,RelationshipLabel
/m/03bt1vf,/m/02wzbmj,is
/m/01y9k5,/m/083vt,is
/m/04yx4,/m/0jyfg,wears
/m/02p5f1q,/m/02vqfm,contain

```

### oidv6-relationships-description.csv

```
at,at
holds,holds
wears,wears
surf,surf
hang,hang
drink,drink
```

### oidv6-train-annotations-bbox.csv

```
$ head oidv6-train-annotations-bbox.csv
ImageID,Source,LabelName,Confidence,XMin,XMax,YMin,YMax,IsOccluded,IsTruncated,IsGroupOf,IsDepiction,IsInside,XClick1X,XClick2X,XClick3X,XClick4X,XClick1Y,XClick2Y,XClick3Y,XClick4Y
000002b66c9c498e,xclick,/m/01g317,1,0.012500,0.195312,0.148438,0.587500,0,1,0,0,0,0.148438,0.012500,0.059375,0.195312,0.148438,0.357812,0.587500,0.325000
000002b66c9c498e,xclick,/m/01g317,1,0.025000,0.276563,0.714063,0.948438,0,1,0,0,0,0.025000,0.248438,0.276563,0.214062,0.914062,0.714063,0.782813,0.948438
000002b66c9c498e,xclick,/m/01g317,1,0.151562,0.310937,0.198437,0.590625,1,0,0,0,0,0.243750,0.151562,0.310937,0.262500,0.198437,0.434375,0.507812,0.590625
```

### train-annotations-human-imagelabels-boxable.csv

```
$ head train-annotations-human-imagelabels-boxable.csv
ImageID,Source,LabelName,Confidence
000002b66c9c498e,verification,/m/014j1m,0
000002b66c9c498e,verification,/m/014sv8,1
000002b66c9c498e,verification,/m/01599,0
000002b66c9c498e,verification,/m/015p6,0
```


### train-images-boxable-with-rotation.csv

```
$ head train-images-boxable-with-rotation.csv
ImageID,Subset,OriginalURL,OriginalLandingURL,License,AuthorProfileURL,Author,Title,OriginalSize,OriginalMD5,Thumbnail300KURL,Rotation
4fa8054781a4c382,train,https://farm3.staticflickr.com/5310/5898076654_51085e157c_o.jpg,https://www.flickr.com/photos/michael-beat/5898076654,https://creativecommons.org/licenses/by/2.0/,https://www.flickr.com/people/michael-beat/,Michael Beat,...die FNF-Kerze,4405052,KFukvivpCM5QXl5SqKe41g==,https://c1.staticflickr.com/6/5310/5898076654_00643a940c_z.jpg,0.0
b37f763ae67d0888,train,https://c1.staticflickr.com/1/67/197493648_628a7cb2ee_o.jpg,https://www.flickr.com/photos/drstarbuck/197493648,https://creativecommons.org/licenses/by/2.0/,https://www.flickr.com/people/drstarbuck/,Karen,Three boys on a hill,494555,9IzEn38GRNsVpATuv7gzEA==,https://c3.staticflickr.com/1/67/197493648_628a7cb2ee_z.jpg?zz=1,0.0
```


### train-annotations-object-segmentation.csv

```
MaskPath,ImageID,LabelName,BoxID,BoxXMin,BoxXMax,BoxYMin,BoxYMax,PredictedIoU,Clicks
677c122b0eaa5d16_m04yx4_9a041d52.png,677c122b0eaa5d16,/m/04yx4,9a041d52,0.8875,0.960938,0.454167,0.720833,0.86864,0.95498 0.65197 1;0.89370 0.56579 1;0.94701 0.48968 0;0.91049 0.70010 1;0.93927 0.47160 1;0.90269 0.56068 0;0.92061 0.70749 0;0.92509 0.64628 0;0.92248 0.65188 1;0.93042 0.46071 1;0.93290 0.71142 1;0.94431 0.48783 0
05529ae018130c68_m09j2d_b1115fd0.png,05529ae018130c68,/m/09j2d,b1115fd0,0.086875,0.254375,0.504708,0.79096,0.8025,0.16388 0.50114 1;0.25069 0.75425 1;0.13478 0.67270 0;0.13478 0.51730 0;0.14134 0.73927 0;0.17918 0.68295 1;0.22580 0.63150 0;0.11365 0.51121 1;0.23104 0.61840 1;0.09115 0.52401 0;0.14678 0.68757 1
96e7ee70b428a54e_m04yx4_05580497.png,96e7ee70b428a54e,/m/04yx4,05580497,0.45625,0.603125,0.222013,0.903104,0.5585,0.52271 0.46625 0;0.52695 0.70150 0;0.59151 0.88178 1;0.49977 0.26807 1;0.48395 0.28952 0;0.55182 0.36076 1;0.50092 0.74922 1;0.58754 0.59330 0;0.50099 0.66845 1;0.56294 0.60185 1;0.50788 0.37395 1;0.52656 0.23633 1
76084f166740d78a_m09j2d_557dfcf5.png,76084f166740d78a,/m/09j2d,557dfcf5,0.01875,0.145625,0.313333,0.754167,0.62394,0.08756 0.34082 0;0.03971 0.34195 1;0.06705 0.65066 1;0.12771 0.66433 0;0.03228 0.40017 0;0.05536 0.72212 1;0.09264 0.65702 0;0.12371 0.75171 0;0.07303 0.36018 1;0.09183 0.64838 0;0.12515 0.33626 1;0.13027 0.73723 1
```
