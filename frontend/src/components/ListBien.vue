<script setup>
import {onMounted, ref} from 'vue'
import {Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot,} from '@headlessui/vue'

// Références pour le formulaire
const isOpen = ref(false)
const listBien = ref([])

// Références pour les champs du formulaire
const form = ref({
  ville: '',
  prix: 0,
  surface: 0,
  note: 0,
  annee: 0,
  garage: false,
})

function closeModal() {
  isOpen.value = false
}

function openModal() {
  isOpen.value = true
}

// Fonction pour charger les biens
async function loadBiens() {
  try {
    const response = await fetch('http://localhost:5001/biens', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    listBien.value = await response.json() // Assigne les données à listBien
  } catch (error) {
    console.error('Error:', error)
  }
}

// Fonction pour ajouter un bien
async function addBien() {
  try {
    const response = await fetch('http://localhost:5001/biens', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form.value)
    })
    if (response.ok) {
      closeModal()
      await loadBiens() // Rafraîchir la liste après ajout
      resetForm() // Réinitialiser le formulaire
    }
  } catch (error) {
    console.error('Error:', error)
  }
}

// Réinitialiser le formulaire après ajout
function resetForm() {
  form.value = {
    ville: '',
    prix: 0,
    surface: 0,
    note: 0,
    annee: 0,
    garage: false,
  }
}

// Charger les biens lors du montage du composant
onMounted(() => {
  loadBiens()
})
</script>
<template>
  <section class="container px-4 mx-auto mt-10">
    <div class="flex justify-between">
      <h2 class="text-lg font-medium text-gray-800 dark:text-white">Liste des biens</h2>

      <a @click="openModal"
         class="group flex items-center px-3 py-2 cursor-pointer text-sm font-medium text-white transition-all duration-200 bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 shadow-md hover:shadow-lg">
        <span class="mr-2">Ajouter un bien</span>
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 256 256"
             class="transition-transform duration-200 group-hover:rotate-90">
          <path d="M222,128a6,6,0,0,1-6,6H134v82a6,6,0,0,1-12,0V134H40a6,6,0,0,1,0-12h82V40a6,6,0,0,1,12,0v82h82A6,6,0,0,1,222,128Z"></path>
        </svg>
      </a>
    </div>

    <div class="flex flex-col mt-6">
      <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
          <div class="overflow-hidden border border-gray-200 dark:border-gray-700 md:rounded-lg">

            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-800">
              <tr>
                <th class="py-3.5 px-4 text-sm font-normal text-left text-gray-500 dark:text-gray-400">Ville</th>
                <th class="px-4 py-3.5 text-sm font-normal text-left text-gray-500 dark:text-gray-400">Prix</th>
                <th class="px-4 py-3.5 text-sm font-normal text-left text-gray-500 dark:text-gray-400">Surface</th>
                <th class="px-4 py-3.5 text-sm font-normal text-left text-gray-500 dark:text-gray-400">Note</th>
                <th class="px-4 py-3.5 text-sm font-normal text-left text-gray-500 dark:text-gray-400">Année</th>
                <th class="px-12 py-3.5 text-sm font-normal text-left text-gray-500 dark:text-gray-400">Garage</th>
              </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200 dark:divide-gray-700 dark:bg-gray-900">
              <tr v-for="(bien, index) in listBien" :key="index">
                <td class="px-4 py-4 text-sm font-normal text-gray-900 dark:text-gray-100">{{ bien.ville }}</td>
                <td class="px-4 py-4 text-sm font-normal text-gray-900 dark:text-gray-100">{{ bien.prix }} €</td>
                <td class="px-4 py-4 text-sm font-normal text-gray-900 dark:text-gray-100">{{ bien.surface }} m²</td>
                <td class="px-4 py-4 text-sm font-normal text-gray-900 dark:text-gray-100">{{ bien.note }}</td>
                <td class="px-4 py-4 text-sm font-normal text-gray-900 dark:text-gray-100">{{ bien.annee }}</td>
                <td class="px-12 py-4 text-sm font-normal text-gray-900 dark:text-gray-100">
                  <span v-if="bien.garage">Oui</span>
                  <span v-else>Non</span>
                </td>
              </tr>
              </tbody>
            </table>

          </div>
        </div>
      </div>
    </div>

  </section>

  <!--  MODAL-->
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" @close="closeModal" class="relative z-10">
      <TransitionChild
          as="template"
          enter="duration-300 ease-out"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="duration-200 ease-in"
          leave-from="opacity-100"
          leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div
            class="flex min-h-full items-center justify-center p-4 text-center"
        >
          <TransitionChild
              as="template"
              enter="duration-300 ease-out"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="duration-200 ease-in"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
          >
            <DialogPanel
                class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                  as="h3"
                  class="text-lg font-medium leading-6 text-gray-900"
              >
                Ajout d'un bien
              </DialogTitle>
              <form @submit.prevent="addBien">
                <div class="grid grid-cols-1 gap-6 mt-4 sm:grid-cols-2">
                  <div>
                    <label class="text-gray-700 dark:text-gray-200" for="ville">Ville</label>
                    <select required v-model="form.ville" id="ville" class="block w-full h-10 px-4 py-1 mt-2 text-gray-700 bg-white border border-gray-200 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-400 focus:ring-blue-300 focus:ring-opacity-40 dark:focus:border-blue-300 focus:outline-none focus:ring">
                      <option value="lyon">Lyon</option>
                      <option value="paris">Paris</option>
                      <option value="marseille">Marseille</option>
                    </select>
                  </div>
                  <div>
                    <label class="text-gray-700 dark:text-gray-200" for="prix">Prix</label>
                    <input required v-model="form.prix" id="prix" type="number" placeholder="100 000€" class="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-200 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-400 focus:ring-blue-300 focus:ring-opacity-40 dark:focus:border-blue-300 focus:outline-none focus:ring">
                  </div>

                  <div>
                    <label class="text-gray-700 dark:text-gray-200" for="surface">Surface</label>
                    <input required v-model="form.surface" id="surface" type="text" placeholder="100" class="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-200 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-400 focus:ring-blue-300 focus:ring-opacity-40 dark:focus:border-blue-300 focus:outline-none focus:ring">
                  </div>

                  <div>
                    <label class="text-gray-700 dark:text-gray-200" for="note">Note</label>
                    <input required v-model="form.note" id="note" type="number" step="1" placeholder="10" class="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-200 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-400 focus:ring-blue-300 focus:ring-opacity-40 dark:focus:border-blue-300 focus:outline-none focus:ring">
                  </div>

                  <div>
                    <label class="text-gray-700 dark:text-gray-200" for="annee">Année</label>
                    <input required v-model="form.annee" id="annee" type="number" placeholder="2020" class="block w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-200 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-400 focus:ring-blue-300 focus:ring-opacity-40 dark:focus:border-blue-300 focus:outline-none focus:ring">
                  </div>


                  <div>
                    <label class="text-gray-700 dark:text-gray-200" for="garage">Garage</label>
                    <input required v-model="form.garage" id="garage" type="checkbox" class="block px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-200 rounded-md dark:bg-gray-800 dark:text-gray-300 dark:border-gray-600 focus:border-blue-400 focus:ring-blue-300 focus:ring-opacity-40 dark:focus:border-blue-300 focus:outline-none focus:ring">
                  </div>

                </div>

                <div class="flex justify-end mt-6">
                  <button type="submit" class="px-8 py-2.5 leading-5 text-white transition-colors duration-300 transform bg-gray-700 rounded-md hover:bg-gray-600 focus:outline-none focus:bg-gray-600">Ajouter</button>
                </div>
              </form>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
