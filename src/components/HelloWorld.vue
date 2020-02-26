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
        <v-btn class="ml-3" small color="primary" @click="update()">Actualizar</v-btn>
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
                      <v-text-field v-model="editedItem.ec_empresa" disabled label="Empresa"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.ec_cliente" disabled label="Cliente"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field
                        v-model="editedItem.ec_rubro_cliente"
                        disabled
                        label="Rubro cliente"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.ec_segmento" disabled label="Segmento"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field
                        v-model="editedItem.ec_tiempo_exp"
                        disabled
                        label="Tiempo exp. (meses)"
                      ></v-text-field>
                    </v-col>
                  </div>
                  <div class="col-12" v-if="editedItem.flag_eo==1">
                    <h2>Otros</h2>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.eo_empresa" disabled label="Empresa"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.eo_rubro_empresa" disabled label="Rubro"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field v-model="editedItem.eo_puesto" disabled label="Puesto"></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="12" md="6">
                      <v-text-field
                        v-model="editedItem.eo_tiempo_exp"
                        disabled
                        label="Tiempo exp. (meses)"
                      ></v-text-field>
                    </v-col>
                  </div>
                </v-row>
              </v-container>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.agended="{ item }">
      <v-checkbox v-model="item.agended" @change="onCheckboxChange(item)"></v-checkbox>
    </template>
    <template v-slot:item.action="{ item }">
      <v-btn small color="primary" @click="editItem(item)">Experiencia</v-btn>
      <!-- <v-icon small @click="deleteItem(item)">delete</v-icon> -->
    </template>
    <!-- <template v-slot:item.check="{ item }">
      <v-btn small color="primary" @click="editItem(item)">Experiencia</v-btn>
      <v-checkbox v-model="checkbox" :label="`Checkbox 1: ${checkbox.toString()}`"></v-checkbox>
      <v-icon small @click="deleteItem(item)">delete</v-icon>
    </template>-->
    <!--
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">Reset</v-btn>
    </template>-->
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
    headers: [
      {
        text: "Nº",
        align: "left",
        value: "number"
      },
      {
        text: "Nombre y apellido",
        value: "name"
      },
      { text: "Correo", value: "email" },
      { text: "Teléfono", value: "phone" },
      { text: "Registro", value: "register" },
      { text: "Formacion", value: "formacion" },
      { text: "Agendad@", value: "agended" },
      { text: "Experiencia", value: "action", sortable: false }
    ],
    editedIndex: -1,
    editedItem: {
      name: "",
      phone: "",
      register: "",
      experience: []
    },
    indexAgended: -1,
    agendedItem: {
      name: "",
      key: "",
      phone: "",
      register: "",
      agended: false,
      experience: []
    },
    defaultItem: {
      name: "",
      email: "",
      phone: "",
      register: "",
      experience: []
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
    onCheckboxChange(item) {
      var updates = {};
      updates["/POSTULANTES/" + item.key + "/agended/"] = item.agended;
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

        if (this.postulantesInfo[postulanteInfo].nombre_social != undefined) {
          if (this.postulantesInfo[postulanteInfo].agended == undefined) {
            postulantes_table = {
              number: i,
              key: postulanteInfo,
              name:
                this.postulantesInfo[postulanteInfo].nombre_social +
                " " +
                this.postulantesInfo[postulanteInfo].apellido_p,
              email: this.postulantesInfo[postulanteInfo].correo,
              phone: this.postulantesInfo[postulanteInfo].telefono,
              register:
                this.postulantesInfo[postulanteInfo].RegistradoDate.date +
                " " +
                this.postulantesInfo[postulanteInfo].RegistradoDate.hour,
              agended: false,
              experience: this.getExperiencePostulante(postulanteInfo)
            };
          } else {
            postulantes_table = {
              number: i,
              key: postulanteInfo,
              name:
                this.postulantesInfo[postulanteInfo].nombre_social +
                " " +
                this.postulantesInfo[postulanteInfo].apellido_p,
              email: this.postulantesInfo[postulanteInfo].correo,
              phone: this.postulantesInfo[postulanteInfo].telefono,
              register:
                this.postulantesInfo[postulanteInfo].RegistradoDate.date +
                " " +
                this.postulantesInfo[postulanteInfo].RegistradoDate.hour,
              agended: this.postulantesInfo[postulanteInfo].agended,
              experience: this.getExperiencePostulante(postulanteInfo)
            };
          }
        } else {
          if (this.postulantesInfo[postulanteInfo].agended == undefined) {
            postulantes_table = {
              number: i,
              key: postulanteInfo,
              name:
                this.postulantesInfo[postulanteInfo].nombres +
                " " +
                this.postulantesInfo[postulanteInfo].apellido_p,
              email: this.postulantesInfo[postulanteInfo].correo,
              phone: this.postulantesInfo[postulanteInfo].telefono,
              register:
                this.postulantesInfo[postulanteInfo].RegistradoDate.date +
                " " +
                this.postulantesInfo[postulanteInfo].RegistradoDate.hour,
              agended: false,
              experience: this.getExperiencePostulante(postulanteInfo)
            };
          } else {
            postulantes_table = {
              number: i,
              key: postulanteInfo,
              name:
                this.postulantesInfo[postulanteInfo].nombres +
                " " +
                this.postulantesInfo[postulanteInfo].apellido_p,
              email: this.postulantesInfo[postulanteInfo].correo,
              phone: this.postulantesInfo[postulanteInfo].telefono,
              register:
                this.postulantesInfo[postulanteInfo].RegistradoDate.date +
                " " +
                this.postulantesInfo[postulanteInfo].RegistradoDate.hour,
              agended: this.postulantesInfo[postulanteInfo].agended,
              experience: this.getExperiencePostulante(postulanteInfo)
            };
          }
        }

        this.postulanteTable.push(postulantes_table);
        let postulanteData = {
          postulanteinfoPersonal: this.postulantesInfo[postulanteInfo],
          postulanteExp: this.getExperiencePostulante(postulanteInfo),
          postulanteProf: this.getFormacionPostulante(postulanteInfo)
        };
        this.postulantes.push(postulanteData);
        i++;
      }
      console.log(this.postulanteTable);
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
    }
  }
};
</script>
