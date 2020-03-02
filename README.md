# Test ImageMaker

Instrucciones para pruebas en local... 
antes de continuar con la instalación asegúrese de que el archivo 
```bash
apiKey.json
```
se encuentre dentro de la carpeta flask.


## Instalación


```bash
$ git clone https://github.com/piedrucci/image_maker.git
$ cd image_maker
$ docker compose up --build

```

## Uso
desde su navegador abrir la siguiente url 
```bash
http://localhost
```
Para probar desde un Cliente Rest como Postman, usar el endpoint 
```bash 
POST http://localhost/check-image
```

se debe enviar un multipart/form-data con el parametro file 
