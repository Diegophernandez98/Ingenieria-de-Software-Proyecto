function Persona2(rut, celular) {
    this.rut = rut;
    this.celular = celular;
};

var selectRut = document.getElementById("id_rut");
Persona2.rut = selectRut.value;
var selectCelular= document.getElementById("id_celular");
Persona2.celular = selectCelular.value;

var errorLength = document.createElement("label");
errorLength.innerText = "Error. Excede el máximo de caracteres permitidos";
var selectDivRut = document.getElementById("idDivRut");
selectDivRut.appendChild(errorLength);
errorLength.style.color = "red";
errorLength.style.display = "none";

var errorLengthCelu = document.createElement("label");
errorLengthCelu.innerText = "Error. Longitud no válida";
var selectDivCelular = document.getElementById("idDivCelular");
selectDivCelular.appendChild(errorLengthCelu);
errorLengthCelu.style.color = "red";
errorLengthCelu.style.display = "none";

function checkRut(rut) {
    var valor = rut.value.replace('.','');
   
    valor = valor.replace('-','');
    
    cuerpo = valor.slice(0,-1);
    dv = valor.slice(-1).toUpperCase();
    
    rut.value = cuerpo + '-'+ dv
    
    if(cuerpo.length < 7) { rut.setCustomValidity("RUT Incompleto"); return false;}

    suma = 0;
    multiplo = 2;
 
    for(i=1;i<=cuerpo.length;i++) {

        index = multiplo * valor.charAt(cuerpo.length - i);

        suma = suma + index;
        
        if(multiplo < 7) { multiplo = multiplo + 1; } else { multiplo = 2; }
  
    }

    dvEsperado = 11 - (suma % 11);
    dv = (dv == 'K')?10:dv;
    dv = (dv == 0)?11:dv;
    
    if(dvEsperado != dv) { rut.setCustomValidity("RUT Inválido"); return false; }

    rut.setCustomValidity('');
}

function guardar(){
    Persona2.rut = selectRut.value;
    console.log(Persona2.rut);

    Persona2.celular = selectCelular.value;
    var celularLength = celularLength.value.length;
    console.log(celularLength);
    if (celularLength > 9 || celularLength < 9){
        celularLength.setCustomValidity("Celular Inválido");
        return false;
    }
}

selectRut.onblur = guardar;