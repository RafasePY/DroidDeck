# DroidDeck Personal — etapa de segurança 1

> **Código experimental, NÃO auditado integralmente, NÃO testado no S25 FE e NÃO comprovado como seguro para credenciais Steam.** Esta branch não inclui um APK aprovado para uso.

## Origem
Fork de [wallentx/DroidDeck](https://github.com/wallentx/DroidDeck), preservando a licença GPL-3.0 e os créditos de quem criou o software.

## Alterações aplicadas
- Removidas as permissões de localização, microfone e instalação de outros APKs. Isso **desativa ou limita** Wi-Fi discovery, entrada de voz e atualização interna.
- Compilações do tipo `release` não usam mais a chave **pública** de testes AOSP: precisam de um certificado PKCS12 **privado**, informado por variáveis de ambiente. `debug` ainda usa a chave de teste; não deve ser distribuído nem usado com conta Steam principal.
- Não foi modificada a autenticação da Steam ou o conteúdo executado dentro do Linux/Proton, nem foram auditadas todas as bibliotecas nativas e dependências baixadas.
- O app mantém `targetSdkVersion 28` por dependência arquitetural: executáveis no diretório privado. Trata-se de risco que exige estudo; atualizar o número isoladamente quebra o runtime.

## Verificação básica do código
```sh
python3 tools/personal/check_security.py
```

## Assinatura local privada (para futuras compilações)
Guarde as chaves FORA do GitHub e nunca compartilhe senhas de assinatura, nem as escreva nos chats.
```sh
keytool -genkeypair -storetype PKCS12 -keystore personal-release.p12 \
    -alias personal -keyalg RSA -keysize 4096 -validity 3650 \
    -dname "CN=DroidDeck Personal"
export DROIDDECK_PERSONAL_KEYSTORE=/CAMINHO/SEGURO/personal-release.p12
export DROIDDECK_PERSONAL_STORE_PASSWORD="SENHA_LOCAL"
export DROIDDECK_PERSONAL_KEY_ALIAS=personal
export DROIDDECK_PERSONAL_KEY_PASSWORD="SENHA_LOCAL"
```
Para compilar, o projeto ainda exige SDK/NDK Android, Java 17, Rust, Docker e os componentes indicados no README original. Nunca inclua chaves no repositório. Após compilar, confira `apksigner verify --verbose --print-certs`, certificado e SHA-256.

## Avisos
1. O pacote `com.droiddeck.launcher` foi mantido para não quebrar caminhos internos. Assinaturas privadas não atualizam instalações existentes assinadas com chave AOSP: **não desinstale sem backup**.
2. A CI herdada do projeto pode gerar APKs de teste usando a chave AOSP. **Não instale artefatos Actions como versão pessoal verificada.** É preciso concluir a adaptação da pipeline para assinar com uma chave privada.
3. O fork foi criado a partir da branch `dev`, cujo README ainda declara GPUs **Xclipse não suportadas**. Compatibilidade Exynos 2400/Xclipse 940 ainda não foi implementada ou testada.
4. Não entre com a conta Steam principal enquanto código, downloads e autenticação não tiverem sido revisados e testados num aparelho de teste.

Esse documento descreve somente a primeira etapa. Nenhuma conclusão de ausência de malware foi estabelecida.
