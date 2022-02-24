# Antes de iniciar
O intuito deste documento é explicar a implementação da arquitetura hexagonal com `FastAPI`, porém, se você nunca teve contato com os conceitos de *Clean Architecture* e *Hexagon Architecure* pode ser interessante que dedique alguns minutos à leitura dos seguintes artigos:
- [Clean and Hexagonal Architectures for Dummies](https://medium.com/codex/clean-architecture-for-dummies-df6561d42c94)
- [Hexagonal Architecture in Python](https://douwevandermeij.medium.com/hexagonal-architecture-in-python-7468c2606b63)

# Arquitetura Hexagonal

Antes de mais nada, vale deixar claro que uma solução mais simples pode muito bem resolver o problema caso o objetivo seja somente receber, gravar e expor dados. E uma solução mais simples deve ser empregada sempre que for possível.
> Simple is better than complex.
> -- The Zen of Python

No entanto, a escolha desta arquitetura foi motivada não por sua simplicidade, mas por características como sua resiliência à mudanças, desacoplamento e testabilidade (estas vantagens são detalhadas na seção [pontos positivos](#vantagens)).

A arquitetura hexagonal foi proposta por [Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/) com o objetivo de "permitir que uma aplicação possa ser utilizada igualmente por usuários, programas, testes automatizados ou *batch scripts*, e ser desenvolvida e testada isolada de eventuais dispositivos ou bancos de dados" ([Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/), tradução livre).

A ideia central é separar o código que contém a lógica da nossa aplicação das tecnologias utilizadas para processamento de entrada e saída, que deverão ser acessadas via *adapters*.

![Exemplo de arquitetura hexagonal. Fonte: [reflectoring.io](https://reflectoring.io/spring-hexagonal/)](https://reflectoring.io/images/posts/spring-hexagonal/hexagonal-architecture_hu6764515d7030d45af6f7f498c79e292b_50897_956x0_resize_box_3.png)
<p align="center">
Exemplo de arquitetura hexagonal. Fonte: <a href="https://reflectoring.io/spring-hexagonal/">reflectoring.io</a>.
</p>

No centro da arquitetura temos o código fundamental para o funcionamento do sistema. Aqui estão nossas entidades e os casos de uso contendo as regras de negócio. Enquanto o código que depende de tecnologias externas (bibliotecas de terceiros, chamadas a APIs, bancos de dados e *etc*.) é posicionado fora através de *adapters*.

No centro, os casos de uso se comunicam com o mundo externo através de portas, que na prática são interfaces que devem ser implementadas pelos *adapters*. Estes por sua vez, são de fato os responsáveis por comunicar a aplicação com outras tecnologias e sistemas.

Neste projeto temos a seguinte organização:
```
└─── adapter
	 └─── db
	 |    |    location_repository_impl.py
	 |    |    location_mapper.py
	 |    |    model.py
	 |    |    sql_db.py
└─── domain
     └─── repository
     │        location_repository.py
     └─── use_cases
     │    │    base_location_use_case.py
     |    │    create_location_use_case.py
     |    │    list_location_use_case.py
     └─── misc
     │    │     exception.py
     |    model.py
main.py
```

Iniciando pelo módulo `domain`, no arquivo [model.py](https://github.com/zehpatricio/fast_api/blob/main/app/domain/model.py) têm-se as entidades que serão manipuladas. No sub-módulo `repository` temos então a interface [location_repository.py](https://github.com/zehpatricio/fast_api/blob/main/app/domain/repository/location_repository.py) que define os métodos `list` e `create` que deverão ser implementados de fato pelos *adapters*. Já em `use_cases` temos os arquivos onde reside a lógica da nossa aplicação. Neste exemplo simples o único processamento feito nos *use cases* são as chamadas ao método equivalente no repositório, mas eles são o núcleo da aplicação, o lugar onde sua regra de negócio deve ser implementada.

Já no módulo `adapter` temos a implementação do [repositório](https://github.com/zehpatricio/fast_api/blob/main/app/adapter/db/location_repository_impl.py), a classe de conexão com o banco de dados [sql_db.py](https://github.com/zehpatricio/fast_api/blob/main/app/adapter/db/sql_db.py), as [entidades de modelo do banco de dados](https://github.com/zehpatricio/fast_api/blob/main/app/adapter/db/model.py), e o [*mapper*](https://github.com/zehpatricio/fast_api/blob/main/app/adapter/db/location_mapper.py) que converte as entidades do `domain` para entidades `sql-alchemy` e vice-versa.

Por fim, o arquivo [main.py](https://github.com/zehpatricio/fast_api/blob/main/main.py) possui as funções do `FastAPI` que disponibilizam os métodos HTTP  GET e POST da API. 
> Nota: os métodos GET e POST são **portas** de entrada da aplicação e seria melhor que estivessem implementados como *adapters*. Como isso iria requerer injeção de dependência dos casos de uso utilizados por eles, por simplicidade, foi feita a opção por mantê-los neste arquivo e instanciar diretamente os casos de uso.

Desta forma temos uma versão simplificada da arquitetura hexagonal com a qual conseguimos criar uma aplicação completa dotada das vantagens da arquitetura.

## Vantagens
### ETC: *Easier To Change*
> Good Design Is Easier to Change Than Bad Design
> -- The Pragmatic Programmer

A facilidade que temos em mudar partes de um sistema sem comprometer o restante dele é um dos princípios do bom *design*. A maior parte do tempo de vida e custos de um *software* são dados com manutenção. Portanto, é importante que mudanças possam ser feitas de forma rápida e fácil.

Este é um dos principais pontos vantajosos neste modelo de arquitetura. Pois com a separação das camadas dependentes de tecnologia externa da camada de lógica, podemos criar sistemas onde a camada de persistência ou camada de entrada podem ser facilmente trocadas. 

Quer um exemplo prático? No *commit* [3756c0](https://github.com/zehpatricio/fast_api/commit/3756c06a8e47c36fd6ae5f2350a3094e1eeb37b7) a biblioteca de acesso ao banco de dados foi mudada de [dataset lib](https://dataset.readthedocs.io/en/latest/) para [SQLAlchemy](https://www.sqlalchemy.org/) e a única mudança fora do módulo de *adapters* foi uma linha no arquivo `main.py`. *Simple like that* =D.

Isto, aliado ao desacoplamento, é um ponto essencial na escolha deste formato de desenvolvimento. Tendo as partes da nossa aplicação separadas, a lógica intocada no domínio, os processos de entrada e saída separados em portas e acessados via *adapters*, podemos facilmente mudar qualquer uma destas partes sem precisar mudar uma só linha de código do demais.

### *Decoupling*
Uma vez que a sua regra de negócio está implementada no seu módulo de domínio, todo o código relacionado à entrada e saída é de responsabilidade de seus *adapters*. Desta forma, se um problema for descoberto na biblioteca que você utiliza para codificar sua API, uma biblioteca melhor for criada, ou você resolve criar uma versão *desktop*, não há necessidade de mudar sua regra de negócio, seu código continua o mesmo e você só precisa de um novo *adapter* de entrada.

Quer um ótimo exemplo disso? Recentemente uma [falha no log4j](https://www.cnnbrasil.com.br/tecnologia/falha-de-seguranca-do-log4j-pode-afetar-toda-a-internet-o-que-voce-precisa-saber/) foi descoberta e a maior parte da *internet* está vulnerável a isto, pois grandes sistemas utilizam o `log4j` por todo seu código. E mesmo que não utilizem diretamente podem utilizar bibliotecas que por baixo dependem do `log4j`.

O problema de existir uma vulnerabilidade uma biblioteca de terceiros que está entranhada nas partes vitais da sua aplicação pode ser um  em quesito de segurança e uma baita dor de cabeça para o time que deverá solucionar isto.

Código desacoplado é fácil de mudar, manter e testar.

### *Testability*
Por fim, graças aos fatores anteriores a arquitetura também facilita os testes. Em um código que não utiliza bibliotecas externas, a lógica de negócio é facilmente verificada. Não existem chamadas a bancos de dados ou escritas em tela a serem *mockadas*, você só se preocupará em testar o **seu código**, suas regras, suas validações e como seu sistema trata os dados de entrada e produz suas saídas. 

Relembremos que o objetivo da arquitetura é "ser desenvolvida e **testada** isolada de eventuais dispositivos ou bancos de dados" ([Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)).

Mas se mesmo assim você precisar testar as chamadas a bancos de dados e *etc*., pode fazer isso separadamente no módulo do seu *adapter*, deixando sua aplicação completamente agnóstica às tecnologias utilizadas na entrada e saída.

## Desvantagens
A principal crítica que se pode fazer talvez seja o grande número de módulos, interfaces e arquivos necessários. Isso pode ser encarado como *boilerplate* já que em aplicações simples como esta não há grande carga de regras e lógica de negócio, e existem muitas classes que somente repassam a informação de um ponto a outro.

Entretanto, toda arquitetura tem este problema em grau maior ou menor, justamente pois a alternativa que removeria completamente qualquer *boilerplate* seria colocar nossas *queries* diretamente no `onClick` dos botões, o que não não é desejável.

Então, tudo bem em escrever mais em mais arquivos se você tiver um código desacoplado, testável e fácil de modificar.

## Melhorias
Embora funcional, a aplicação ainda tem algumas possíveis melhorias que, por conta do tempo e da finalidade, não foram implementadas:
- **Testes**: a prática de TDD é altamente recomendada para melhoria da qualidade de código em geral, e também é facilitada pelas características da arquitetura escolhida. Porém, para agilizar o processo não foram criados testes.
- ***Mappers* na camada de entrada**: assim como os [mappers](https://github.com/zehpatricio/fast_api/blob/main/app/adapter/db/location_mapper.py) que transformam os modelos de domínio dos modelos de persistência, devem ser criados *mappers* da camada de entrada para a camada de domínio. Desta forma, poderíamos ter um código no módulo de domínio completamente isolado de quaisquer bibliotecas ou artefatos de terceiros. O que não é o caso aqui pois nossas [classes de modelo](https://github.com/zehpatricio/fast_api/blob/main/app/domain/model.py)  possuem referências a outras bibliotecas (`pydantic` por exemplo). Além de aumentar o nível de acoplamento do código, este tipo de dependência pode representar um risco futuro à aplicação.

### That's all, folks!
