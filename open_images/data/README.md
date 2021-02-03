## Descrição dos dados:

**Dataset**: Open Images Dataset V6

Arquivos baixados em https://storage.googleapis.com/openimages/web/download.html

Instruções em https://storage.googleapis.com/openimages/web/factsfigures.html


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
