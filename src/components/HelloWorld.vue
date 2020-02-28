<template>
  <!-- <p v-if="loginState">Hola</p> -->
  <login v-if="loginState" v-on:validate="getLoginState($event)"></login>
  <v-data-table
    v-else
    :headers="headers"
    :items="postulanteTable"
    sort-by="number"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Postulantes Vivekonecta</v-toolbar-title>
        <v-btn class="ml-3" small color="success" @click="update()">Actualizar</v-btn>
        <v-divider class="mx-4" inset vertical></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <!-- <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="mb-2" v-on="on">New Item</v-btn>
          </template>-->
          <v-card>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cerrar</v-btn>
            </v-card-actions>
            <v-card-title>
              <span class="headline">{{ formTitle }} {{editedItem.name}}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row v-for="(editedItem, index) in editedItem.experience" v-bind:key="index">
                  <p v-if="editedItem.flag_se==1">No tiene experiencia</p>
                  <div class="col-12" v-if="editedItem.flag_ec==1">
                    <h2>En Call</h2>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.ec_empresa" label="Empresa"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.ec_cliente" label="Cliente"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.ec_rubro_cliente" label="Rubro cliente"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.ec_segmento" label="Segmento"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.ec_tiempo_exp" label="Tiempo exp. (meses)"></v-text-field>
                    </v-col>
                  </div>
                  <div class="col-12" v-if="editedItem.flag_eo==1">
                    <h2>Otros</h2>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.eo_empresa" label="Empresa"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.eo_rubro_empresa" label="Rubro"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.eo_puesto" label="Puesto"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.eo_tiempo_exp" label="Tiempo exp. (meses)"></v-text-field>
                    </v-col>
                  </div>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-dialog>
        <v-dialog v-model="cardForm" max-width="500px">
          <v-card>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeForm">Cerrar</v-btn>
            </v-card-actions>
            <v-card-title>
              <span class="headline">Datos Profesionales de {{formItem.name}}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <p v-if="formItem.postulanteProf==undefined">No tiene formación</p>
                <v-row v-else class="col-12">
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field
                      v-model="formItem.postulanteProf.grado_formacion"
                      label="Grado de formación"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field v-model="formItem.postulanteProf.institucion" label="Institución"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field
                      v-model="formItem.postulanteProf.estado_estudios"
                      label="Estado de estudio"
                    ></v-text-field>
                  </v-col>
                  <v-col
                    v-if="formItem.postulanteProf.horario_estudio!=undefined"
                    cols="12"
                    sm="12"
                    md="6"
                  >
                    <v-text-field
                      v-model="formItem.postulanteProf.horario_estudio"
                      label="Horario de estudio"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field
                      v-model="formItem.postulanteProf.rubro_carrera"
                      label="Rubro de carrera"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-dialog>
        <v-dialog v-model="cardInfo" max-width="500px">
          <v-card>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeInfo">Cerrar</v-btn>
            </v-card-actions>
            <v-card-title>
              <span class="headline">Datos personales de {{infoItem.name}}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row class="col-12">
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field
                      class="inpuInfo"
                      v-model="infoItem.infoPersonal.telefono"
                      label="Teléfono"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field v-model="infoItem.infoPersonal.correo" label="Correo"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field v-model="infoItem.infoPersonal.estado_civil" label="Estado civil"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field
                      v-model="infoItem.infoPersonal.fecha_nac"
                      label="Fecha de nacimiento"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="6">
                    <v-text-field v-model="infoItem.infoPersonal.genero" label="Género"></v-text-field>
                  </v-col>
                  <v-col v-if="infoItem.infoPersonal.text_dir==undefined " cols="12" sm="12" md="6">
                    <v-text-field label="Dirección"></v-text-field>
                  </v-col>
                  <v-col v-else cols="12" sm="12" md="6">
                    <v-text-field v-model="infoItem.infoPersonal.text_dir" label="Dirección"></v-text-field>
                  </v-col>
                  <v-col v-if="infoItem.infoPersonal.n_hijos==undefined " cols="12" sm="12" md="6">
                    <v-text-field value="No tiene" label="Hij@s"></v-text-field>
                  </v-col>
                  <v-col v-else cols="12" sm="12" md="6">
                    <v-text-field v-model="infoItem.infoPersonal.n_hijos" label="Hij@s"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.infoPersonal="{ item }">
      <v-btn small color="info" @click="infoCard(item)">Info postulante</v-btn>
      <!-- <v-icon small @click="deleteItem(item)">delete</v-icon> -->
    </template>
    <template v-slot:item.formacion="{ item }">
      <v-btn small color="info" @click="formacionCard(item)">Formacion</v-btn>
      <!-- <v-icon small @click="deleteItem(item)">delete</v-icon> -->
    </template>

    <template v-slot:item.action="{ item }">
      <v-btn small color="info" @click="editItem(item)">Experiencia</v-btn>
      <!-- <v-icon small @click="deleteItem(item)">delete</v-icon> -->
    </template>
    <template v-slot:item.agended="{ item }">
      <v-checkbox v-model="item.agended" @change="onCheckboxChange(item)"></v-checkbox>
    </template>
    <template v-slot:item.espontaneo="{ item }">
      <v-checkbox v-model="item.espontaneo" @change="onEspontaneoChange(item)"></v-checkbox>
    </template>
  </v-data-table>
</template>

<script>
import firebase from "firebase";
import login from "./login.vue";

export default {
  name: "HelloWorld",
  components: {
    login
  },

  data: () => ({
    postulantes: [],
    postulanteTable: [],
    postulantesInfo: {},
    postulantesExp: {},
    postulantesProf: {},
    loginState: true,
    dialog: false,
    cardForm: false,
    cardInfo: false,
    headers: [
      {
        text: "Nº",
        align: "left",
        value: "number"
      },
      {
        text: "Tipo Doc",
        value: "tipoDoc"
      },
      {
        text: "Nº Doc",
        value: "numDoc"
      },
      {
        text: "Nombre y apellido",
        value: "name"
      },
      { text: "Datos postulante", value: "infoPersonal", sortable: false },
      { text: "Formacion", value: "formacion", sortable: false },
      { text: "Experiencia", value: "action", sortable: false },
      { text: "Agendad@", value: "agended" },
      // { text: "Selector@", value: "selectore" },
      { text: "Espontáneo", value: "espontaneo" },
      // { text: "Disponibilidad", value: "disponibilidad" },
      // { text: "Resultado", value: "result" },
      // { text: "IGC", value: "igc" },
      { text: "Registro", value: "register" }
    ],
    editedIndex: -1,
    editedItem: {
      tipoDoc: "",
      numDoc: "",
      name: "",
      key: "",
      register: "",
      infoPersonal: {},
      formacion: {},
      espontaneo: false,
      result: "",
      agended: false,
      experience: []
      // selectore: "",
      // disponitilidad: "",
      // igc: "",
    },
    formIndex: -1,
    formItem: {
      tipoDoc: "",
      numDoc: "",
      name: "",
      key: "",
      register: "",
      infoPersonal: {},
      formacion: {},
      espontaneo: false,
      result: "",
      agended: false,
      experience: []
      // selectore: "",
      // disponitilidad: "",
      // igc: "",
    },
    infoIndex: -1,
    infoItem: {
      tipoDoc: "",
      numDoc: "",
      name: "",
      key: "",
      register: "",
      infoPersonal: {},
      formacion: {},
      espontaneo: false,
      result: "",
      agended: false,
      experience: []
      // selectore: "",
      // disponitilidad: "",
      // igc: "",
    },
    defaultItem: {
      tipoDoc: "",
      numDoc: "",
      name: "",
      key: "",
      register: "",
      infoPersonal: {},
      formacion: {},
      espontaneo: false,
      result: "",
      agended: false,
      experience: []
      // selectore: "",
      // disponitilidad: "",
      // igc: "",
    }
  }),

  computed: {
    formTitle() {
      // return this.editedIndex === -1 ? "New Item" : "Edit Item";
      return "Datos Experiencia:";
    }
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    cardForm(val) {
      val || this.closeForm();
    },
    cardInfo(val) {
      val || this.closeInfo();
    }
  },

  created() {
    this.writeUserData();
    this.writeUserExp();
    this.writeUserProf();
  },
  mounted() {},

  methods: {
    // onCheckboxChange(newValue) {
    //   const title = "VALUE: " + (newValue ? "TRUE" : "FALSE");
    //   console.log(title);
    // },
    editItem(item) {
      this.editedIndex = this.postulanteTable.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },
    formacionCard(item) {
      this.formIndex = this.postulanteTable.indexOf(item);
      this.formItem = Object.assign({}, item);
      this.cardForm = true;
    },
    infoCard(item) {
      this.infoIndex = this.postulanteTable.indexOf(item);
      this.infoItem = Object.assign({}, item);
      this.cardInfo = true;
    },
    onCheckboxChange(item) {
      var updates = {};
      updates["/POSTULANTES/" + item.key + "/agended/"] = item.agended;
      firebase
        .database()
        .ref()
        .update(updates);
    },
    onEspontaneoChange(item) {
      var updates = {};
      updates["/POSTULANTES/" + item.key + "/espontaneo/"] = item.espontaneo;
      firebase
        .database()
        .ref()
        .update(updates);
    },

    deleteItem(item) {
      const index = this.postulanteTable.indexOf(item);
      confirm("Are you sure you want to delete this item?") &&
        this.postulanteTable.splice(index, 1);
    },

    close() {
      this.dialog = false;
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      }, 300);
    },
    closeForm() {
      this.cardForm = false;
      setTimeout(() => {
        this.formItem = Object.assign({}, this.defaultItem);
        this.formIndex = -1;
      }, 300);
    },
    closeInfo() {
      this.cardInfo = false;
      setTimeout(() => {
        this.infoItem = Object.assign({}, this.defaultItem);
        this.infoIndex = -1;
      }, 300);
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.postulanteTable[this.editedIndex], this.editedItem);
      } else {
        this.postulanteTable.push(this.editedItem);
      }
      this.close();
    },
    writeUserData() {
      let postulantes = firebase.database().ref("POSTULANTES");
      postulantes.on("value", this.getPostulant, this.dataUserErr);
    },
    getPostulant(data) {
      this.postulantesInfo = data.val();
    },
    dataUserErr(err) {
      console.log("error");
      console.log(err);
    },
    writeUserExp() {
      let postulantesExp = firebase.database().ref("DATOS_EXPERIENCIA");
      postulantesExp.on("value", this.getPostulantExp, this.dataUserExpErr);
    },
    getPostulantExp(data) {
      this.postulantesExp = data.val();
    },
    dataUserExpErr(err) {
      console.log("error");
      console.log(err);
    },
    writeUserProf() {
      let postulantesProf = firebase.database().ref("DATOS_PROFESIONALES");
      postulantesProf.on("value", this.getPostulantProf, this.dataUserProfErr);
    },
    getPostulantProf(data) {
      this.postulantesProf = data.val();
    },
    dataUserProfErr(err) {
      console.log("error");
      console.log(err);
    },
    getPostulantData() {
      let i = 1;
      for (let postulanteInfo in this.postulantesInfo) {
        let postulantes_table;
        postulantes_table = {
          number: i,
          tipoDoc: this.postulantesInfo[postulanteInfo].tipodoc,
          numDoc: this.postulantesInfo[postulanteInfo].numdoc,
          key: postulanteInfo,
          name: this.getNamePostulante(this.postulantesInfo[postulanteInfo]),
          register:
            this.postulantesInfo[postulanteInfo].RegistradoDate.date +
            " " +
            this.postulantesInfo[postulanteInfo].RegistradoDate.hour,
          agended: this.getAgendedPostulante(
            this.postulantesInfo[postulanteInfo]
          ),
          // state: this.getStatePostulante(
          //   this.postulantesInfo[postulanteInfo]
          // ),
          espontaneo: this.getEspontaneoPostulante(
            this.postulantesInfo[postulanteInfo]
          ),
          infoPersonal: this.postulantesInfo[postulanteInfo],
          experience: this.getExperiencePostulante(postulanteInfo),
          postulanteProf: this.getFormacionPostulante(postulanteInfo)
        };

        this.postulanteTable.push(postulantes_table);
        let postulanteData = {
          postulanteinfoPersonal: this.postulantesInfo[postulanteInfo],
          postulanteExp: this.getExperiencePostulante(postulanteInfo),
          postulanteProf: this.getFormacionPostulante(postulanteInfo)
        };
        this.postulantes.push(postulanteData);
        i++;
      }
      // console.log(this.postulantes);
      // console.log(this.postulanteTable);
    },
    getLoginState: function(loginState) {
      this.loginState = loginState;
      this.getPostulantData();
    },
    getExperiencePostulante(id_postulante) {
      let postulanteExperiences = [];
      for (let postulanteExp in this.postulantesExp) {
        if (id_postulante == this.postulantesExp[postulanteExp].id_postulante) {
          postulanteExperiences.push(this.postulantesExp[postulanteExp]);
        }
      }
      return postulanteExperiences;
    },
    getFormacionPostulante(id_postulante) {
      let postulanteProfesion;
      for (let postulanteProf in this.postulantesProf) {
        if (
          id_postulante == this.postulantesProf[postulanteProf].id_postulante
        ) {
          postulanteProfesion = this.postulantesProf[postulanteProf];
          return postulanteProfesion;
        }
      }
    },
    update() {
      this.writeUserData();
      this.writeUserExp();
      this.writeUserProf();
      this.postulanteTable = [];
      this.getPostulantData();
    },
    getNamePostulante(postulanteInfo) {
      let name;
      if (postulanteInfo.nombre_social != undefined) {
        name = postulanteInfo.nombre_social + " " + postulanteInfo.apellido_p;
      } else {
        name = postulanteInfo.nombres + " " + postulanteInfo.apellido_p;
      }
      return name;
    },
    getAgendedPostulante(postulanteInfo) {
      let agended;
      if (postulanteInfo.agended == undefined) {
        agended = false;
      } else {
        agended = postulanteInfo.agended;
      }
      return agended;
    },
    getEspontaneoPostulante(postulanteInfo) {
      let espontaneo;
      if (postulanteInfo.espontaneo == undefined) {
        espontaneo = false;
      } else {
        espontaneo = postulanteInfo.espontaneo;
      }
      return espontaneo;
    }
    // getStatePostulante(postulanteInfo){
    //   let state;
    //   if(postulanteInfo.state==undefined){
    //     state=false
    //   }else{

    //     if(postulanteInfo.state.agended.active==1){

    //     }

    //   }
    // }
  }
};
</script>

<style>
</style>
