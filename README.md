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
# API

## Models

### Meme
- iud
- link
- name
- idUser
- comentarios
- likes
- dislikes

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

### /getRandom GET
- response
  + array:Memes

### /getComments:memeUid GET
- response
  + array:Comment

### /getReactions:memeUid GET
- response
  + likes
  + dislikes

### /createUser POST
- body:
  + uid
  + nombre
  + email
  + link

### /createMeme POST
- body:
  + nombre
  + idUser
  + link

### /createComment POST
- body:
  + uidMeme
  + comment

### /reaction POST
`Anadir tags a usuario`
- body:
  + type:int  (like=0,dislike=1)
  + uidMeme
  + uidUser 
 
