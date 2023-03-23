<template>
  <v-container>
    <!-- Gemeinde Auswahl -->
    <v-row class="text-center">
      <v-col cols="12">
        <v-autocomplete
          deletable-chips
          filled
          :items="municipalities"
          label="Gemeinde"
        ></v-autocomplete>
      </v-col>
    </v-row>
    <!-- Gemeinde Auswahl END -->
    <v-row>
      <v-col>
        <v-btn color="primary" elevation="2" outlined @click="addRow"
          >Neuer Eintrag</v-btn
        ></v-col
      >
    </v-row>

    <!-- FORMULAR -->
    <v-row>
      <v-form ref="form" v-model="valid" lazy-validation>
        <v-row v-for="row in formData" :key="row.id">
          <!-- Garbage Type -->
          <v-col>
            <v-select
              v-model="row.type"
              :items="garbageType"
              :rules="[(v) => !!v || 'Bitte einen Typ auswählen.']"
              label="Typ"
              required
            ></v-select>
          </v-col>
          <!-- Garbage Type END -->
          <v-col>
            <v-checkbox
              v-model="row.isDateSeries"
              label="Entsorgungsserie?"
            ></v-checkbox>
          </v-col>
          <v-row>
            <!-- Date-Series -->
            <v-row v-if="row.isDateSeries">
              <v-col>
                <v-select
                  v-model="row.value"
                  :items="days"
                  attach
                  chips
                  label="Wann?"
                  multiple
                ></v-select>
                <v-text-field
                  v-model="row.repetition"
                  label="Wiederholung jede(n):"
                  type="number"
                  :rules="[numberRule]"
                ></v-text-field>
                <v-radio-group v-model="row.radioGroup">
                  <v-radio label="Tag(e)" value="days"></v-radio>
                  <v-radio label="Woche(n)" value="weeks"></v-radio>
                  <v-radio label="Monat(e)" value="months"></v-radio>
                  <v-radio label="Jahr(e)" value="years"></v-radio>
                </v-radio-group>
              </v-col>
            </v-row>
          </v-row>
          <!-- Date-Series END -->
          <v-row>
              <!-- Single Datetime -->
              <v-row v-if="!row.isDateSeries">
                <v-col>
                  <v-date-picker
                    v-model="row.datePicker"
                    label="Wähle das Datum"
                  ></v-date-picker>
                </v-col>
                <v-col>
                  <v-time-picker
                    v-model="row.timePicker"
                    label="Wähle die Zeit"
                    format="24hr"
                  ></v-time-picker>
                </v-col>
            </v-row>
          </v-row>
        </v-row>
        <!-- Single Datetime END -->
        <v-row>
          <v-col>
            <!-- Preview -->
            <v-textarea
              readonly
              filled
              label="Vorschau"
              auto-grow
              :value="JSON.stringify(formData)"
            >
              {{ formData }}</v-textarea
            ></v-col
          >
        </v-row>
        <!-- Preview END -->
        <v-btn
          :disabled="!valid"
          color="success"
          class="mr-4"
          @click="downloadAsCSV"
        >
          Download
        </v-btn>
        <v-btn color="error" class="mr-4" @click="reset"> Reset </v-btn>
      </v-form>
    </v-row>
    <!-- FORMULAR END -->
  </v-container>
</template>

<script>
export default {
  name: "HelloWorld",

  data: () => ({
    formData: [],
    municipalities: [
      "Bülach",
      "Lausanne",
      "Chur",
      "Bitsch",
      "Sarnen",
      "Zollikofen",
    ],
    valid: true,
    garbageType: ["Abfall", "Papier", "Sperrgut", "Holz"],
    picker: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
      .toISOString()
      .substr(0, 10),
    days: [
      "Montag",
      "Dienstag",
      "Mittwoch",
      "Donnerstag",
      "Freitag",
      "Samstag",
      "Sonntag",
    ],
    numberRule: (v) => {
      if (!v.trim()) return true;
      if (!isNaN(parseFloat(v)) && v > 0) return true;
      return "Anzahl muss eine positive Nummer sein";
    },
  }),
  methods: {
    addRow() {
      this.formData.push({
        id: new Date().valueOf(),
        type: true,
        isDateSeries: true,
        value: null,
        repetition: "0",
        radioGroup: null,
        datePicker: "",
        timePicker: "",
      });
    },
    /* TODO: DOWNLOAD AS CSV */
    downloadAsCSV() {
      console.log(JSON.stringify(this.formData));
    },
    reset() {
      while (this.formData.length > 0) {
        this.formData.pop();
      }
      this.$refs.form.reset();
    },
  },
};
</script>
