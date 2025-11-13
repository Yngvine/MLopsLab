#let conf(doc) = [

// Document configuration
#set page(
  numbering: "1",
  number-align: center,
  margin: (top: 2.5cm, bottom: 2.5cm, left: 2cm, right: 2cm)
)
#set par(
  first-line-indent: (amount: 1em, all: true),
  spacing: 0.65em,
  justify: true,
)
#show par: it => [
  #it
  #v(0.5em)
]
#set list(
  indent: 1.25em,
  spacing: 0.65em,
)

#set heading(numbering: "1.1.1")

#show heading.where(level:1): it => [
  #it
  #v(0.5cm)
]

#show heading.where(level:2): it => [
  #it
  #v(0.25cm)
]

#show heading.where(level:3): it => [
  #v(0.25cm)
  #it
  #v(0.25cm)
]

#show figure: it => [
  #v(0.25cm)
  #it
  #v(0.25cm)
]
#doc
]
