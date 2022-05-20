function hate_speech_detector(){
	var data = new FormData();
	var request = new XMLHttpRequest();
    const text = document.getElementById("msgc").value;
    console.log(text);
	//Adicionar type
	console.log(getCookie("csrftoken"));
	data.append('csrfmiddlewaretoken', getCookie("csrftoken"));
	data.append('text', text);
	console.log("ESTOU AQUI, APÓS O CSRFTOKEN");
	// AJAX request finished
	request.addEventListener('load', function(e) {
		// Resposta
		console.log(request)
		if(request.status == 200){
			console.log("AJAX import: Successo!");
			console.log(request.response.HateSpeech);
			if (request.response.HateSpeech == "yes"){
				const a = document.getElementById("HateSpeech-detected").innerHTML = '<p class="HateSpeech-detected-p" style="color: red"><i class="bi bi-hand-thumbs-down"></i> Discurso de ódio detectado!</p>\n<p align="justify" class="ms-5">O discurso de ódio fere, diretamente, os direitos de todo e qualquer cidadão - de acordo com a Organização das Nações Unidas (ONU), os direitos humanos são “inerentes a todos os seres humanos, independentemente de raça, sexo, nacionalidade, etnia, idioma, religião ou qualquer outra condição”, incluindo “o direito à vida e à liberdade, à liberdade de opinião e de expressão, o direito ao trabalho e à educação, entre e muitos outros. Todos merecem estes direitos, sem discriminação”.</p>';

			}else if (request.response.HateSpeech == "no"){
				const a = document.getElementById("HateSpeech-detected").innerHTML = '<p style="color: green;"><i class="bi bi-hand-thumbs-up"></i> Discurso de ódio não detectado!</p>';
			}else {
				console.log("Erro inesperado!");
			}

		}else{
			console.log("AJAX import: erro!")
		}
	});

	request.responseType = 'json';
	// Caminho
	request.open('post', `/HateSpeech/`, true);
	request.send( data );
}
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}