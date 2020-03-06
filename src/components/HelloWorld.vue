<template>
  <!-- <p v-if="loginState">Hola</p> -->
  <login v-if="loginState" v-on:validate="getLoginState($event)"></login>
  <v-data-table
    v-else
    :headers="headers"
    :search="search"
    :items="postulanteTable"
    sort-by="number"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Postulantes Vivekonecta</v-toolbar-title>
        <div class="flex-row-mobile">
          <div class="flex-row padding-mobile">
            <v-btn class="ml-3" small color="success" @click="update()">Actualizar</v-btn>
            <v-divider class="mx-4" inset vertical></v-divider>
            <download-csv :data="downloadExcel(postulanteTable)" name="ReporteTotal.csv">
              <v-btn color="blue darken-1" class="padding-0" text>Descargar excel</v-btn>
            </download-csv>
          </div>

          <v-text-field
            class="padding-mobile margin-mobile"
            v-model="search"
            append-icon="mdi-magnify"
            label="Buscar"
            single-line
            hide-details
          ></v-text-field>
        </div>

        <!-- <v-spacer></v-spacer> -->
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
        <v-dialog v-model="cardDisponibilidad" max-width="500px">
          <v-card>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDisponibilidad()">Cerrar</v-btn>
            </v-card-actions>
            <v-card-title>
              <span class="headline">Editar disponibilidad de {{disponibilidadItem.name}}</span>
            </v-card-title>

            <v-card-text>
              <div class="col-12 content-hours">
                <v-col style="flex: 0 1 auto;" cols="12">
                  <h2>Inicio:</h2>
                  <v-time-picker
                    width="200"
                    v-model="disponibilidad.start"
                    :max="disponibilidad.end"
                  ></v-time-picker>
                </v-col>
                <v-col style="flex: 0 1 auto;" cols="12">
                  <h2>Fin:</h2>
                  <v-time-picker
                    width="200"
                    v-model="disponibilidad.end"
                    :min="disponibilidad.start"
                  ></v-time-picker>
                </v-col>
              </div>

              <v-btn
                small
                color="info"
                @click="postDisponibilidad(disponibilidadItem, disponibilidad.start, disponibilidad.end)"
              >Guardar</v-btn>
            </v-card-text>
          </v-card>
        </v-dialog>
        <v-dialog v-model="cardState" max-width="500px">
          <v-card>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeState()">Cerrar</v-btn>
            </v-card-actions>
            <v-card-title>
              <span class="headline">Editar estado de postulación de:</span>
              <hr />
              <span>{{stateItem.name}}</span>
            </v-card-title>

            <v-card-text>
              <div class="col-12 content-hours">
                <v-select
                  v-model="select"
                  :items="items"
                  item-text="track"
                  item-value="track"
                  label="Seleccionar"
                  persistent-hint
                  return-object
                  single-line
                ></v-select>
                <v-btn small color="info" @click="postState(stateItem, select)">Guardar</v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-dialog>
        <v-dialog v-model="cardComments" max-width="500px">
          <v-card>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeComments()">Cerrar</v-btn>
            </v-card-actions>
            <v-card-title>
              <span class="headline">Observaciones de postulante:</span>
              <hr />
              <span>{{commentsItem.name}}</span>
            </v-card-title>

            <v-card-text>
              <div class="col-12 content-hours">
                <div v-if="addCommentState==false">
                  <div v-if="commentsItem.comments.length==0">
                    <p>No hay observaciones</p>
                  </div>
                  <div v-else>
                    <div v-for="(comments, idx) in commentsItem.comments" :key="idx">
                      <p>
                        &#8226; {{comments.comment}}
                        <span
                          class="dateAndHour"
                        >({{comments.date}} a las {{comments.hour}})</span>
                      </p>
                    </div>
                  </div>
                  <v-btn small color="info" @click="postComment()">Añadir</v-btn>
                </div>

                <v-col cols="12" md="6" v-else>
                  <v-textarea
                    solo
                    name="input-7-4"
                    label="Escriba su observación"
                    v-model="textarea"
                  ></v-textarea>
                  <v-btn small color="info" @click="addComment(commentsItem)">Guardar</v-btn>
                </v-col>
              </div>
            </v-card-text>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <br />
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
    <template v-slot:item.state="{ item }">
      <div class="edit-time">
        <v-btn text icon color="blue lighten-2" @click="editStateItem(item)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <p class="margin-0">{{item.state}}</p>
      </div>
    </template>
    <template v-slot:item.espontaneo="{ item }">
      <v-checkbox v-model="item.espontaneo" @change="onEspontaneoChange(item)"></v-checkbox>
    </template>
    <template v-slot:item.disponibilidad="{ item }">
      <v-btn
        v-if="item.disponibilidad.start==null && item.disponibilidad.end==null && item.stateDispo==false"
        small
        color="success"
        @click="addDisponibilidad(item)"
      >Agregar</v-btn>
      <div class="edit-time" v-else>
        <p class="margin-0">{{item.disponibilidad.start}} - {{item.disponibilidad.end}}</p>
        <v-btn text icon color="blue lighten-2" @click="addDisponibilidad(item)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
      </div>
    </template>
    <template v-slot:item.comments="{ item }">
      <v-btn small color="success" @click="addCommentsItem(item)">Ver</v-btn>
    </template>
  </v-data-table>
</template>

<script>
import firebase from "firebase";
import login from "./login.vue";
import moment from "moment";
import Vue from "vue";
import JsonCSV from "vue-json-csv";
Vue.component("downloadCsv", JsonCSV);

export default {
  name: "HelloWorld",
  components: {
    login
  },

  data: () => ({
    textarea: "",
    addCommentState: false,
    search: "",
    select: { track: "No contactad@" },
    items: [
      { track: "Agendad@" },
      { track: "Desestimad@" },
      { track: "En sala de espera" },
      { track: "Evaluad@ - Aprobad@" },
      { track: "Evaluad@ - Rechazad@" },
      { track: "Selección express" }
    ],
    postulantes: [],
    postulanteTable: [],
    postulantesInfo: {},
    postulantesExp: {},
    postulantesProf: {},
    loginState: true,
    dialog: false,
    cardForm: false,
    cardInfo: false,
    cardDisponibilidad: false,
    cardState: false,
    cardComments: false,
    disponibilidad: {
      start: null,
      end: null
    },

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
      { text: "Estado", value: "state" },
      // { text: "Selector@", value: "selectore" },
      { text: "Espontáneo", value: "espontaneo" },
      { text: "Disponibilidad", value: "disponibilidad" },
      // { text: "Resultado", value: "result" },
      // { text: "IGC", value: "igc" },
      { text: "Observación", value: "comments", sortable: false },
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
      state: "",
      comments: [],

      experience: [],
      // selectore: "",
      disponibilidad: {}
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
      state: "",
      comments: [],
      // agended: false,
      experience: [],
      // selectore: "",
      disponibilidad: {}
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
      state: "",
      comments: [],
      // agended: false,
      experience: [],
      // selectore: "",
      disponibilidad: {}
      // igc: "",
    },
    disponibilidadIndex: -1,
    disponibilidadItem: {
      tipoDoc: "",
      numDoc: "",
      name: "",
      key: "",
      register: "",
      infoPersonal: {},
      formacion: {},
      espontaneo: false,
      result: "",
      state: "",
      comments: [],
      // agended: false,
      experience: [],
      // selectore: "",
      disponibilidad: {}
      // igc: "",
    },
    stateIndex: -1,
    stateItem: {
      tipoDoc: "",
      numDoc: "",
      name: "",
      key: "",
      register: "",
      infoPersonal: {},
      formacion: {},
      espontaneo: false,
      result: "",
      state: "",
      comments: [],
      // agended: false,
      experience: [],
      // selectore: "",
      disponibilidad: {}
      // igc: "",
    },

    commentsIndex: -1,
    commentsItem: {
      tipoDoc: "",
      numDoc: "",
      name: "",
      key: "",
      register: "",
      infoPersonal: {},
      formacion: {},
      espontaneo: false,
      result: "",
      state: "",
      comments: [],
      // agended: false,
      experience: [],
      // selectore: "",
      disponibilidad: {}
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
      state: "",
      comments: [],
      // agended: false,
      experience: [],
      // selectore: "",
      disponibilidad: {}
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
    },
    cardDisponibilidad(val) {
      val || this.closeDisponibilidad();
    },
    cardState(val) {
      val || this.closeState();
    },
    cardComments(val) {
      val || this.closeComments();
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
    addDisponibilidad(item) {
      this.disponibilidadIndex = this.postulanteTable.indexOf(item);
      this.disponibilidadItem = Object.assign({}, item);
      this.cardDisponibilidad = true;
    },
    editStateItem(item) {
      this.stateIndex = this.postulanteTable.indexOf(item);
      this.stateItem = Object.assign({}, item);
      this.cardState = true;
    },
    addCommentsItem(item) {
      this.commentsIndex = this.postulanteTable.indexOf(item);
      this.commentsItem = Object.assign({}, item);
      this.cardComments = true;
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
      // let date = new Date();
      // let dateString = moment().format("L");
      // let hour = date.getHours() + ":" + date.getMinutes() + "";

      // let espontaneo = {
      //   date: dateString,
      //   hour: hour
      // };
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
    closeDisponibilidad() {
      this.cardDisponibilidad = false;
      this.disponibilidad = {
        start: null,
        end: null
      };
      setTimeout(() => {
        this.disponibilidadItem = Object.assign({}, this.defaultItem);
        this.disponibilidadIndex = -1;
      }, 300);
    },
    closeState() {
      this.cardState = false;
      setTimeout(() => {
        this.stateItem = Object.assign({}, this.defaultItem);
        this.stateIndex = -1;
      }, 300);
    },
    closeComments() {
      this.cardComments = false;
      this.addCommentState = false;
      this.textarea = "";
      setTimeout(() => {
        this.commentsItem = Object.assign({}, this.defaultItem);
        this.commentsIndex = -1;
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
          // agended: this.getAgendedPostulante(
          //   this.postulantesInfo[postulanteInfo]
          // ),
          state: this.getStatePostulante(this.postulantesInfo[postulanteInfo]),
          espontaneo: this.getEspontaneoPostulante(
            this.postulantesInfo[postulanteInfo]
          ),
          disponibilidad: this.getDisponibilidadPostulante(
            this.postulantesInfo[postulanteInfo]
          ),
          stateDispo: this.getStateDispo(this.postulantesInfo[postulanteInfo]),
          infoPersonal: this.postulantesInfo[postulanteInfo],
          comments: this.getCommentsPostulante(
            this.postulantesInfo[postulanteInfo].comments
          ),
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
      // console.log(this.postulanteTable);
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
    },
    getDisponibilidadPostulante(postulanteInfo) {
      let disponibilidad;
      if (postulanteInfo.disponibilidad == undefined) {
        disponibilidad = {
          start: null,
          end: null
        };
      } else {
        disponibilidad = postulanteInfo.disponibilidad;
      }
      return disponibilidad;
    },
    getStateDispo(postulanteInfo) {
      let state;
      if (postulanteInfo.disponibilidad == undefined) {
        state = false;
      } else {
        state = true;
      }
      return state;
    },
    postDisponibilidad(item, start, end) {
      var updates = {};
      item.disponibilidad.start = start;
      item.disponibilidad.end = end;
      updates["/POSTULANTES/" + item.key + "/disponibilidad/"] =
        item.disponibilidad;
      firebase
        .database()
        .ref()
        .update(updates);
      item.stateDispo = true;
      this.disponibilidad = {
        start: null,
        end: null
      };
      this.cardDisponibilidad = false;
    },
    getStatePostulante(postulanteInfo) {
      let state;
      if (postulanteInfo.state == undefined) {
        if (postulanteInfo.agended) {
          state = "Agendad@";
        } else {
          state = "No contactad@";
        }
      } else {
        if (postulanteInfo.agended == undefined) {
          if (postulanteInfo.state.agended != undefined) {
            if (postulanteInfo.state.agended.active) {
              state = "Agendad@";
            }
          }
          if (postulanteInfo.state.waiting != undefined) {
            if (postulanteInfo.state.waiting.active) {
              state = "En sala de espera";
            }
          }

          if (postulanteInfo.state.express != undefined) {
            if (postulanteInfo.state.express.active) {
              state = "Selección express";
            }
          }

          if (postulanteInfo.state.approved != undefined) {
            if (postulanteInfo.state.approved.active) {
              state = "Evaluad@ - Aprobad@";
            }
          }

          if (postulanteInfo.state.disapproved != undefined) {
            if (postulanteInfo.state.disapproved.active) {
              state = "Evaluad@ - Rechazad@";
            }
          }
          if (postulanteInfo.state.desestimar != undefined) {
            if (postulanteInfo.state.desestimar.active) {
              state = "Desestimad@";
            }
          }
        } else {
          if (postulanteInfo.agended) {
            state = "Agendad@";
          }

          if (postulanteInfo.state.agended != undefined) {
            if (postulanteInfo.state.agended.active) {
              state = "Agendad@";
            }
          }
          if (postulanteInfo.state.waiting != undefined) {
            if (postulanteInfo.state.waiting.active) {
              state = "En sala de espera";
            }
          }

          if (postulanteInfo.state.express != undefined) {
            if (postulanteInfo.state.express.active) {
              state = "Selección express";
            }
          }

          if (postulanteInfo.state.approved != undefined) {
            if (postulanteInfo.state.approved.active) {
              state = "Evaluad@ - Aprobad@";
            }
          }

          if (postulanteInfo.state.disapproved != undefined) {
            if (postulanteInfo.state.disapproved.active) {
              state = "Evaluad@ - Rechazad@";
            }
          }
          if (postulanteInfo.state.desestimar != undefined) {
            if (postulanteInfo.state.desestimar.active) {
              state = "Desestimad@";
            }
          }
        }
      }
      return state;
    },
    postState(postulanteInfo, state) {
      var updates = {};
      let oldState = postulanteInfo.state;
      let date = new Date();
      let dateString = moment().format("L");
      let hour = date.getHours() + ":" + date.getMinutes() + "";

      let editState = {
        active: true,
        date: dateString,
        hour: hour
      };

      this.offOldState(postulanteInfo, oldState);

      if (state.track == "Agendad@") {
        updates[
          "/POSTULANTES/" + postulanteInfo.key + "/state/agended/"
        ] = editState;
        firebase
          .database()
          .ref()
          .update(updates);

        if (postulanteInfo.agended != undefined) {
          var update = {};
          update["/POSTULANTES/" + postulanteInfo.key + "/agended/"] = true;
          firebase
            .database()
            .ref()
            .update(update);
        }
        this.update();
      } else {
        if (state.track == "En sala de espera") {
          updates[
            "/POSTULANTES/" + postulanteInfo.key + "/state/waiting/"
          ] = editState;
          firebase
            .database()
            .ref()
            .update(updates);

          this.update();
        } else {
          if (state.track == "Selección express") {
            updates[
              "/POSTULANTES/" + postulanteInfo.key + "/state/express/"
            ] = editState;
            firebase
              .database()
              .ref()
              .update(updates);
            this.update();
          } else {
            if (state.track == "Evaluad@ - Aprobad@") {
              updates[
                "/POSTULANTES/" + postulanteInfo.key + "/state/approved/"
              ] = editState;
              firebase
                .database()
                .ref()
                .update(updates);
              this.update();
            } else {
              if (state.track == "Evaluad@ - Rechazad@") {
                updates[
                  "/POSTULANTES/" + postulanteInfo.key + "/state/disapproved/"
                ] = editState;
                firebase
                  .database()
                  .ref()
                  .update(updates);
                this.update();
              } else {
                if (state.track == "Desestimad@") {
                  updates[
                    "/POSTULANTES/" + postulanteInfo.key + "/state/desestimar/"
                  ] = editState;
                  firebase
                    .database()
                    .ref()
                    .update(updates);
                  this.update();
                }
              }
            }
          }
        }
      }

      this.cardState = false;
    },
    offOldState(postulanteInfo, oldState) {
      // console.log(oldState);
      var updates = {};
      if (oldState == "Agendad@") {
        updates[
          "/POSTULANTES/" + postulanteInfo.key + "/state/agended/active/"
        ] = false;
        firebase
          .database()
          .ref()
          .update(updates);
        if (postulanteInfo.agended) {
          var update = {};
          update["/POSTULANTES/" + postulanteInfo.key + "/agended/"] = false;
          firebase
            .database()
            .ref()
            .update(update);
        }
      } else {
        if (oldState == "En sala de espera") {
          updates[
            "/POSTULANTES/" + postulanteInfo.key + "/state/waiting/active/"
          ] = false;
          firebase
            .database()
            .ref()
            .update(updates);
        } else {
          if (oldState == "Selección express") {
            updates[
              "/POSTULANTES/" + postulanteInfo.key + "/state/express/active/"
            ] = false;
            firebase
              .database()
              .ref()
              .update(updates);
          } else {
            if (oldState == "Evaluad@ - Aprobad@") {
              updates[
                "/POSTULANTES/" + postulanteInfo.key + "/state/approved/active/"
              ] = false;
              firebase
                .database()
                .ref()
                .update(updates);
            } else {
              if (oldState == "Evaluad@ - Rechazad@") {
                updates[
                  "/POSTULANTES/" +
                    postulanteInfo.key +
                    "/state/disapproved/active/"
                ] = false;
                firebase
                  .database()
                  .ref()
                  .update(updates);
              } else {
                if (oldState == "Desestimad@") {
                  updates[
                    "/POSTULANTES/" +
                      postulanteInfo.key +
                      "/state/desestimar/active/"
                  ] = false;
                  firebase
                    .database()
                    .ref()
                    .update(updates);
                }
              }
            }
          }
        }
      }
    },
    downloadExcel(postulanteTable) {
      let dataTotal = [];

      for (let i = 0; i < postulanteTable.length; i++) {
        // dataTotal.push({
        //   Nº: postulanteTable[i].number,
        //   "Tipo de documento": postulanteTable[i].tipoDoc,
        //   "Nº de documento": postulanteTable[i].numDoc,
        //   "Nombre/Nombre social completo": postulanteTable[i].name,
        //   "Fecha y hora de registro": postulanteTable[i].register
        // });

        for (let u = 0; u < postulanteTable[i].experience.length; u++) {
          if (postulanteTable[i].postulanteProf != undefined) {
            dataTotal.push({
              Nº: postulanteTable[i].number,
              "Tipo de documento": postulanteTable[i].tipoDoc,
              "Nº de documento": postulanteTable[i].numDoc,
              "Nombres completos": postulanteTable[i].infoPersonal.nombres,
              "Apellido paterno": postulanteTable[i].infoPersonal.apellido_p ,
              "Apellido materno": postulanteTable[i].infoPersonal.apellido_m ,
              "Nombre/Nombre social": postulanteTable[i].name,
              "Estado de postulacion": postulanteTable[i].state,
              "Estado civil": postulanteTable[i].infoPersonal.estado_civil,
              "Fecha de nacimiento": postulanteTable[i].infoPersonal.fecha_nac,
              Género: postulanteTable[i].infoPersonal.genero,
              "Nº de hijos": postulanteTable[i].infoPersonal.n_hijos,
              "Correo electrónico": postulanteTable[i].infoPersonal.correo,
              Teléfono: postulanteTable[i].infoPersonal.telefono,
              Dirección: postulanteTable[i].infoPersonal.text_dir,
              "Fecha y hora de registro": postulanteTable[i].register,
              "Grado de formacion":
                postulanteTable[i].postulanteProf.grado_formacion,
              "Estado estudio":
                postulanteTable[i].postulanteProf.estado_estudios,
              Institucion: postulanteTable[i].postulanteProf.institucion,
              "Rubro carrera": postulanteTable[i].postulanteProf.rubro_carrera,
              "Horario estudio":
                postulanteTable[i].postulanteProf.horario_estudio,
              "Empresa - experiencia no call":
                postulanteTable[i].experience[u].eo_empresa,
              "Rubro empresa - experiencia no call":
                postulanteTable[i].experience[u].eo_rubro_empresa,
              "Puesto experiencia - no call":
                postulanteTable[i].experience[u].eo_puesto,
              "Tiempo (meses) - experiencia no call":
                postulanteTable[i].experience[u].eo_tiempo_exp,
              "Empresa - experiencia call":
                postulanteTable[i].experience[u].ec_empresa,
              "Cliente - experiencia call":
                postulanteTable[i].experience[u].ec_cliente,
              "Rubro cliente - experiencia call":
                postulanteTable[i].experience[u].ec_rubro_cliente,
              "Segmento - experiencia call":
                postulanteTable[i].experience[u].ec_segmento,
              "Tiempo (meses) - experiencia call":
                postulanteTable[i].experience[u].ec_tiempo_exp,
              "Disponibilidad horaria":
                postulanteTable[i].disponibilidad.start +
                "-" +
                postulanteTable[i].disponibilidad.end,
              Espontáneo: postulanteTable[i].espontaneo
            });
          }
        }
      }

      // for (let i = 0; i < postulanteTable.experience.length; i++) {
      //   dataTotal.push({
      //     Nº: postulanteTable[i].number,
      //     "Tipo de documento": postulanteTable[i].tipoDoc,
      //     "Nº de documento": postulanteTable[i].numDoc,
      //     "Nombre/Nombre social completo": postulanteTable[i].name,
      //     "Fecha y hora de registro": postulanteTable[i].register
      //   });
      // }

      return dataTotal;
    },
    getCommentsPostulante(comments) {
      let seleccionComments = [];
      if (comments != undefined) {
        seleccionComments = comments;
      } else {
        return seleccionComments;
      }
      return seleccionComments;
    },
    postComment() {
      this.addCommentState = true;
    },
    addComment(commentsItem) {
      var updates = {};
      let newComment = this.textarea;

      let date = new Date();
      let dateString = moment().format("L");
      let hour = date.getHours() + ":" + date.getMinutes() + "";

      let editComments = {
        comment: newComment,
        date: dateString,
        hour: hour
      };
      commentsItem.comments.push(editComments);
    

      updates["/POSTULANTES/" + commentsItem.key + "/comments/"] =
        commentsItem.comments;
      firebase
        .database()
        .ref()
        .update(updates);

      this.addCommentState = false;
      this.textarea = "";
    }
  }
};
</script>

<style>
.content-hours {
  display: flex;
  align-content: center;
  justify-content: center;
  flex-direction: row;
  padding: 0 !important;
}
.edit-time {
  display: flex;
  flex-direction: row;
  justify-content: stretch;
  align-content: center;
  align-items: center;
}

.margin-0 {
  margin: 0 !important;
}
.padding-0 {
  padding: 0 !important;
}
.flex-row {
  display: flex;
  flex-direction: row;
}

.flex-row-mobile {
  display: flex;
  flex-direction: row;
}
.margin-mobile {
  margin-left: 2em;
}
.dateAndHour {
  font-size: 0.8em !important;
  color: #4e5056 !important;
}

@media (max-width: 767px) {
  .content-hours {
    flex-direction: column;
  }

  .flex-row-mobile {
    flex-direction: column;
  }

  .margin-mobile {
    margin: 1.5em;
  }

  .padding-mobile {
    padding-top: 3em;
  }

  .v-data-table table {
    margin-top: 3em !important;
  }
}
</style>
