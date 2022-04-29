#!/bin/bash

function show_box()
{
	SHOW_BOX_MSG=$1
	SHOW_BOX_L=${#SHOW_BOX_MSG}
	SHOW_BOX_L=$((SHOW_BOX_L+4))
	SHOW_BOX_LINE=""
	for SHOW_BOX_i in $(seq $SHOW_BOX_L)
	do
		SHOW_BOX_LINE=${SHOW_BOX_LINE}"-"
	done
	echo
	echo ${SHOW_BOX_LINE}
	echo \| $SHOW_BOX_MSG \|
	echo ${SHOW_BOX_LINE}
	echo
}

case $1 in


	1) show_box "Envio de e-mail com imagem em anexo"
		nome_imagem="image.png" # imagem pessoa detectada
		email_from="from@gmail.com"
		passw_from="frompswd"
		email_to="to@gmail.com"
		servidor_envio="smtp://smtp.gmail.com:587"
		criptografia="--ssl"
		email_subject="Alerta de seguranca raspberry pi"
		email_msg="Camera detectou pessoa!"
		echo "From: <$email_from>" > email.txt
		echo "To: <$email_to>" >> email.txt
		echo Subject: $email_subject >> email.txt
		echo Date: $(date) >> email.txt
		echo Content-Type: multipart/mixed\; boundary=corpo_msg >> email.txt
		echo >> email.txt
		echo --corpo_msg >> email.txt
		echo Content-Type: text/plain\; charset=UTF-8 >> email.txt
		echo >> email.txt
		echo $email_msg >> email.txt
		echo >> email.txt
		echo --corpo_msg >> email.txt
		echo Content-Type: image/png\; name=\"$nome_imagem\" >> email.txt
		echo Content-Transfer-Encoding: base64 >> email.txt
		echo Content-Disposition: attachment; filename=\"$nome_imagem\" >> email.txt
		echo >> email.txt
		cat $nome_imagem | base64 >> email.txt
		echo --corpo_msg-- >> email.txt
		curl -u $email_from:$passw_from -n -v --mail-from $email_from --mail-rcpt $email_to --url $servidor_envio $criptografia -T email.txt
		show_box "Este foi o arquivo usado para enviar o e-mail"
		cat email.txt
		rm email.txt;;
		*) echo "Opção inválida";;
		
		
esac
