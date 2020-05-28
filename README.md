# Deep Memes backend services

### Tecnologies

Flask - Python

### Mantainers

- [quirinoc](https://github.com/quirinoc)
- [Razonixx](https://github.com/razonixx)

## Setup

```sh
sh build.sh
sh run.sh
```
## TASKS FRONT END
 - [PACO] REMPLAZAR POPULAR -> RANDOM
 - [PACO] WHO TO FOLLOW -> PROFILE
 - [PACO] UI PROFILE 
      + LIKES
      + COMMENTS
 - [PACO] MEJORAR UI AUTH
 - [PACO] MEJORAR MEMECARD
 - [RICKY] SUBIR MEMES
 - [RICKY] COMENTARIOS Y LIKES
 - [RICKY] ACTUALIZAR TAGS

# API

## Models

### Meme
- uid
- link
- title
- idUser
- comentarios
- likes
- dislikes
- tags

### User
- uid
- nombre
- link
- tags
- email

## Methods

### /getUser:uid GET
- response
  + email
  + tags
  + nombre
  + link

### /getRelatedTo:tags GET 
- response
  + array:Memes

### /getRandom GET [PACO] (REMPLAZAR POPULAR -> RANDOM)
- response
  + array:Memes

### /getComments:memeUid GET [RICKY]
- response
  + array:Comment

### /getReactions:memeUid GET [RICKY]
- response
  + likes
  + dislikes

### /createUser POST [RICKY]
- body:
  + uid
  + nombre
  + email
  + link

### /createMeme POST [RICKY]
- body:
  + nombre
  + idUser
  + link

### /createComment POST [RICKY]
- body:
  + uidMeme
  + comment

### /reaction POST [RICKY]
`Anadir tags a usuario`
- body:
  + type:int  (like=0,dislike=1)
  + uidMeme
  + uidUser 
 
