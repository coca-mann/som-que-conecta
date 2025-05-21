<template>
    <div class="min-h-screen flex flex-col bg-gray-50">
        <!-- Navbar -->
        <header class="bg-emerald-700 text-white shadow-md">
            <div class="container mx-auto px-4 py-3">
                <div class="flex flex-col md:flex-row md:justify-between md:items-center">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center">
                            <music-icon class="h-8 w-8 mr-2" />
                            <span class="text-xl font-bold">MusicaMaster</span>
                        </div>
                        <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden">
                            <menu-icon v-if="!mobileMenuOpen" class="h-6 w-6" />
                            <x-icon v-else class="h-6 w-6" />
                        </button>
                    </div>

                    <nav :class="{ 'hidden': !mobileMenuOpen, 'flex': mobileMenuOpen }"
                        class="flex-col md:flex md:flex-row mt-4 md:mt-0">
                        <a v-for="(item, index) in navItems" :key="index"
                            @click="currentPage = item.route; mobileMenuOpen = false"
                            :class="{ 'bg-emerald-800': currentPage === item.route }"
                            class="px-4 py-2 rounded-md hover:bg-emerald-800 transition-colors cursor-pointer mb-1 md:mb-0 md:mr-1">
                            {{ item.name }}
                        </a>

                        <!-- User menu for logged in users -->
                        <div v-if="isLoggedIn" class="relative">
                            <button @click="userMenuOpen = !userMenuOpen"
                                class="flex items-center px-4 py-2 rounded-md hover:bg-emerald-800 transition-colors cursor-pointer mb-1 md:mb-0 md:mr-1">
                                <user-icon class="h-5 w-5 mr-1" />
                                <span>{{ userType === 'student' ? 'Minha Conta' : 'Área do Voluntário' }}</span>
                            </button>

                            <div v-if="userMenuOpen"
                                class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
                                <a @click="currentPage = 'profile'; userMenuOpen = false"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer">
                                    Perfil
                                </a>
                                <a v-if="userType === 'volunteer'"
                                    @click="currentPage = 'manage-instruments'; userMenuOpen = false"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer">
                                    Gerenciar Instrumentos
                                </a>
                                <a v-if="userType === 'volunteer'"
                                    @click="currentPage = 'manage-schedule'; userMenuOpen = false"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer">
                                    Gerenciar Agenda
                                </a>
                                <a @click="isLoggedIn = false; userMenuOpen = false"
                                    class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer">
                                    Sair
                                </a>
                            </div>
                        </div>

                        <!-- Login button for guests -->
                        <a v-if="!isLoggedIn" @click="showLoginModal = true"
                            class="px-4 py-2 rounded-md bg-emerald-600 hover:bg-emerald-500 transition-colors cursor-pointer mt-2 md:mt-0 md:ml-2">
                            Entrar
                        </a>
                    </nav>
                </div>
            </div>
        </header>

        <!-- Login Modal -->
        <div v-if="showLoginModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-6 w-full max-w-md">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-bold">Entrar</h2>
                    <button @click="showLoginModal = false" class="text-gray-500 hover:text-gray-700">
                        <x-icon class="h-5 w-5" />
                    </button>
                </div>

                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                        <input type="email" v-model="loginEmail"
                            class="w-full px-3 py-2 border border-gray-300 rounded-md" placeholder="seu@email.com" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Senha</label>
                        <input type="password" v-model="loginPassword"
                            class="w-full px-3 py-2 border border-gray-300 rounded-md" placeholder="********" />
                    </div>
                    <div class="flex items-center">
                        <input type="checkbox" id="user-type" v-model="isVolunteerLogin"
                            class="h-4 w-4 text-emerald-600 border-gray-300 rounded" />
                        <label for="user-type" class="ml-2 block text-sm text-gray-700">
                            Entrar como ONG/Professor Voluntário
                        </label>
                    </div>
                    <div class="flex justify-between">
                        <button @click="login"
                            class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                            Entrar
                        </button>
                        <button class="text-emerald-600 hover:text-emerald-500">
                            Esqueci minha senha
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <main class="flex-grow container mx-auto px-4 py-8">
            <!-- Home Page -->
            <div v-if="currentPage === 'home'" class="space-y-8">
                <section class="text-center py-12">
                    <h1 class="text-4xl md:text-5xl font-bold text-emerald-800 mb-4">Aprenda Música no Seu Ritmo</h1>
                    <p class="text-lg text-gray-600 max-w-2xl mx-auto">
                        Descubra o mundo dos instrumentos musicais e desenvolva suas habilidades com nossos cursos e
                        recursos.
                    </p>
                    <button @click="currentPage = 'courses'"
                        class="mt-6 px-6 py-3 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                        Explorar Cursos
                    </button>
                </section>

                <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-white rounded-lg shadow-md overflow-hidden">
                        <div class="h-48 bg-emerald-200 flex items-center justify-center">
                            <book-open-icon class="h-16 w-16 text-emerald-700" />
                        </div>
                        <div class="p-4">
                            <h3 class="text-xl font-semibold mb-2">Artigos Públicos</h3>
                            <p class="text-gray-600 mb-4">Confira nossos artigos sobre teoria musical e técnicas de
                                aprendizado.</p>
                            <button @click="currentPage = 'articles'" class="text-emerald-600 hover:text-emerald-500">
                                Ver Artigos →
                            </button>
                        </div>
                    </div>

                    <div class="bg-white rounded-lg shadow-md overflow-hidden">
                        <div class="h-48 bg-amber-200 flex items-center justify-center">
                            <music-icon class="h-16 w-16 text-amber-700" />
                        </div>
                        <div class="p-4">
                            <h3 class="text-xl font-semibold mb-2">Instrumentos Musicais</h3>
                            <p class="text-gray-600 mb-4">Explore nossa coleção de instrumentos disponíveis para
                                aprendizado.</p>
                            <button @click="currentPage = 'instruments'"
                                class="text-emerald-600 hover:text-emerald-500">
                                Ver Instrumentos →
                            </button>
                        </div>
                    </div>

                    <div class="bg-white rounded-lg shadow-md overflow-hidden">
                        <div class="h-48 bg-rose-200 flex items-center justify-center">
                            <graduation-cap-icon class="h-16 w-16 text-rose-700" />
                        </div>
                        <div class="p-4">
                            <h3 class="text-xl font-semibold mb-2">Mini-Cursos</h3>
                            <p class="text-gray-600 mb-4">Comece a aprender com nossos mini-cursos para iniciantes.</p>
                            <button @click="currentPage = 'courses'" class="text-emerald-600 hover:text-emerald-500">
                                Ver Cursos →
                            </button>
                        </div>
                    </div>
                </section>

                <section class="bg-white rounded-lg shadow-md p-6">
                    <h2 class="text-2xl font-bold mb-4">Atualizações Recentes</h2>
                    <div class="space-y-4">
                        <div v-for="(update, index) in recentUpdates" :key="index" class="border-b pb-4 last:border-0">
                            <div class="flex items-start">
                                <div class="bg-emerald-100 p-2 rounded-md mr-4">
                                    <component :is="update.icon" class="h-5 w-5 text-emerald-600" />
                                </div>
                                <div>
                                    <h3 class="font-semibold">{{ update.title }}</h3>
                                    <p class="text-gray-600">{{ update.description }}</p>
                                    <span class="text-sm text-gray-500">{{ update.date }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>

            <!-- Articles Section - Public -->
            <div v-else-if="currentPage === 'articles'" class="space-y-6">
                <h1 class="text-3xl font-bold text-emerald-800 mb-6">Artigos sobre Música</h1>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div v-for="(article, index) in articles" :key="index"
                        class="bg-white rounded-lg shadow-md overflow-hidden">
                        <div
                            class="h-48 bg-gradient-to-r from-emerald-400 to-teal-500 flex items-center justify-center">
                            <component :is="article.icon" class="h-16 w-16 text-white" />
                        </div>
                        <div class="p-4">
                            <span
                                class="inline-block px-2 py-1 bg-emerald-100 text-emerald-800 rounded-md text-sm mb-2">{{
                                article.category }}</span>
                            <h3 class="text-xl font-semibold mb-2">{{ article.title }}</h3>
                            <p class="text-gray-600 mb-4">{{ article.excerpt }}</p>
                            <div class="flex justify-between items-center">
                                <span class="text-sm text-gray-500">{{ article.date }}</span>
                                <button class="text-emerald-600 hover:text-emerald-500">Ler mais →</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Instruments Section - Private -->
            <div v-else-if="currentPage === 'instruments'" class="space-y-8">
                <h1 class="text-3xl font-bold text-emerald-800 mb-6">Instrumentos Musicais</h1>

                <!-- Login required message -->
                <div v-if="!isLoggedIn" class="bg-amber-50 border border-amber-200 rounded-lg p-6 text-center">
                    <lock-icon class="h-12 w-12 text-amber-500 mx-auto mb-4" />
                    <h2 class="text-xl font-semibold mb-2">Acesso Restrito</h2>
                    <p class="text-gray-600 mb-4">Faça login para acessar informações sobre instrumentos disponíveis e
                        gerenciar seus instrumentos.</p>
                    <button @click="showLoginModal = true"
                        class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                        Entrar
                    </button>
                </div>

                <!-- Instruments content for logged in users -->
                <div v-else>
                    <section>
                        <h2 class="text-2xl font-semibold mb-4">Seus Instrumentos</h2>
                        <div v-if="myInstruments.length === 0" class="bg-gray-100 rounded-lg p-6 text-center">
                            <music-icon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
                            <p class="text-gray-600">Você ainda não possui instrumentos registrados.</p>
                        </div>
                        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                            <div v-for="(instrument, index) in myInstruments" :key="index"
                                class="bg-white rounded-lg shadow-md p-4">
                                <div class="h-40 bg-gray-100 rounded-md flex items-center justify-center mb-3">
                                    <component :is="instrument.icon" class="h-16 w-16 text-emerald-600" />
                                </div>
                                <h3 class="font-semibold">{{ instrument.name }}</h3>
                                <p class="text-sm text-gray-500">Adicionado em {{ instrument.addedDate }}</p>
                            </div>
                        </div>
                    </section>

                    <section class="mt-8">
                        <h2 class="text-2xl font-semibold mb-4">Instrumentos Disponíveis</h2>
                        <div class="bg-white rounded-lg shadow-md p-4">
                            <div class="mb-4">
                                <label class="block text-sm font-medium text-gray-700 mb-1">Filtrar por:</label>
                                <div class="flex flex-wrap gap-2">
                                    <button v-for="(source, index) in ['Todos', 'ONGs', 'Professores']" :key="index"
                                        :class="{ 'bg-emerald-600 text-white': instrumentFilter === source, 'bg-gray-100 text-gray-800': instrumentFilter !== source }"
                                        class="px-3 py-1 rounded-md text-sm" @click="instrumentFilter = source">
                                        {{ source }}
                                    </button>
                                </div>
                            </div>

                            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                                <div v-for="(instrument, index) in filteredAvailableInstruments" :key="index"
                                    class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                                    <div class="flex items-center mb-3">
                                        <component :is="instrument.icon" class="h-8 w-8 text-emerald-600 mr-2" />
                                        <h3 class="font-semibold">{{ instrument.name }}</h3>
                                    </div>
                                    <p class="text-sm text-gray-600 mb-2">{{ instrument.description }}</p>
                                    <div class="flex justify-between items-center">
                                        <span class="text-xs px-2 py-1 bg-emerald-100 text-emerald-800 rounded-full">{{
                                            instrument.source }}</span>
                                        <button
                                            @click="currentPage = 'instrument-schedule'; selectedInstrument = instrument"
                                            class="text-sm text-emerald-600 hover:text-emerald-500">
                                            Ver Disponibilidade
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            </div>

            <!-- Courses Section - Private -->
            <div v-else-if="currentPage === 'courses'" class="space-y-6">
                <h1 class="text-3xl font-bold text-emerald-800 mb-6">Mini-Cursos para Iniciantes</h1>

                <!-- Login required message -->
                <div v-if="!isLoggedIn" class="bg-amber-50 border border-amber-200 rounded-lg p-6 text-center">
                    <lock-icon class="h-12 w-12 text-amber-500 mx-auto mb-4" />
                    <h2 class="text-xl font-semibold mb-2">Acesso Restrito</h2>
                    <p class="text-gray-600 mb-4">Faça login para acessar nossos mini-cursos e começar sua jornada
                        musical.</p>
                    <button @click="showLoginModal = true"
                        class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                        Entrar
                    </button>
                </div>

                <!-- Courses content for logged in users -->
                <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div v-for="(course, index) in courses" :key="index"
                        class="bg-white rounded-lg shadow-md overflow-hidden"
                        @click="currentPage = 'course-detail'; selectedCourse = course">
                        <div class="h-48 bg-gradient-to-r from-emerald-500 to-teal-600 relative">
                            <div class="absolute inset-0 flex items-center justify-center">
                                <component :is="course.icon" class="h-20 w-20 text-white" />
                            </div>
                            <div
                                class="absolute top-2 right-2 bg-white rounded-full px-2 py-1 text-xs font-medium text-emerald-700">
                                {{ course.level }}
                            </div>
                        </div>
                        <div class="p-4">
                            <h3 class="text-xl font-semibold mb-2">{{ course.title }}</h3>
                            <p class="text-gray-600 mb-4">{{ course.description }}</p>
                            <div class="flex items-center justify-between mb-4">
                                <div class="flex items-center">
                                    <clock-icon class="h-4 w-4 text-gray-500 mr-1" />
                                    <span class="text-sm text-gray-500">{{ course.duration }}</span>
                                </div>
                                <div class="flex items-center">
                                    <users-icon class="h-4 w-4 text-gray-500 mr-1" />
                                    <span class="text-sm text-gray-500">{{ course.students }} alunos</span>
                                </div>
                            </div>

                            <!-- Progress bar for enrolled courses -->
                            <div v-if="course.enrolled" class="mb-4">
                                <div class="flex justify-between text-sm mb-1">
                                    <span>Progresso</span>
                                    <span>{{ course.progress }}%</span>
                                </div>
                                <div class="w-full bg-gray-200 rounded-full h-2.5">
                                    <div class="bg-emerald-600 h-2.5 rounded-full"
                                        :style="{ width: course.progress + '%' }"></div>
                                </div>
                            </div>

                            <button
                                class="w-full py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                                {{ course.enrolled ? 'Continuar' : 'Iniciar Curso' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Course Detail Page - NEW -->
            <div v-else-if="currentPage === 'course-detail'" class="space-y-6">
                <div class="flex items-center mb-6">
                    <button @click="currentPage = 'courses'" class="mr-4 p-2 rounded-full hover:bg-gray-100">
                        <arrow-left-icon class="h-5 w-5" />
                    </button>
                    <h1 class="text-3xl font-bold text-emerald-800">{{ selectedCourse.title }}</h1>
                </div>

                <div class="bg-white rounded-lg shadow-md overflow-hidden">
                    <div class="h-64 bg-gradient-to-r from-emerald-500 to-teal-600 relative">
                        <div class="absolute inset-0 flex items-center justify-center">
                            <component :is="selectedCourse.icon" class="h-32 w-32 text-white" />
                        </div>
                    </div>

                    <div class="p-6">
                        <div class="flex flex-wrap gap-2 mb-4">
                            <span class="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-sm">
                                {{ selectedCourse.level }}
                            </span>
                            <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm flex items-center">
                                <clock-icon class="h-4 w-4 mr-1" />
                                {{ selectedCourse.duration }}
                            </span>
                            <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm flex items-center">
                                <users-icon class="h-4 w-4 mr-1" />
                                {{ selectedCourse.students }} alunos
                            </span>
                        </div>

                        <p class="text-gray-600 mb-6">{{ selectedCourse.description }}</p>

                        <!-- Progress tracking -->
                        <div class="mb-6">
                            <div class="flex justify-between text-sm mb-1">
                                <span class="font-medium">Seu progresso</span>
                                <span>{{ selectedCourse.progress }}%</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2.5">
                                <div class="bg-emerald-600 h-2.5 rounded-full"
                                    :style="{ width: selectedCourse.progress + '%' }"></div>
                            </div>
                        </div>

                        <!-- Lessons list -->
                        <div class="space-y-4">
                            <h2 class="text-xl font-semibold">Lições</h2>

                            <div v-for="(lesson, index) in selectedCourse.lessons" :key="index"
                                class="border rounded-lg overflow-hidden">
                                <div class="flex items-center justify-between p-4 cursor-pointer"
                                    :class="{ 'bg-gray-50': lesson.completed }"
                                    @click="lesson.expanded = !lesson.expanded">
                                    <div class="flex items-center">
                                        <div class="w-8 h-8 rounded-full flex items-center justify-center mr-3"
                                            :class="lesson.completed ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'">
                                            <check-icon v-if="lesson.completed" class="h-5 w-5" />
                                            <span v-else>{{ index + 1 }}</span>
                                        </div>
                                        <div>
                                            <h3 class="font-medium">{{ lesson.title }}</h3>
                                            <p class="text-sm text-gray-500">{{ lesson.duration }}</p>
                                        </div>
                                    </div>
                                    <chevron-down-icon class="h-5 w-5 text-gray-400 transition-transform"
                                        :class="{ 'transform rotate-180': lesson.expanded }" />
                                </div>

                                <div v-if="lesson.expanded" class="p-4 border-t">
                                    <p class="text-gray-600 mb-4">{{ lesson.description }}</p>

                                    <div v-if="lesson.video"
                                        class="bg-gray-100 h-48 mb-4 flex items-center justify-center">
                                        <play-icon class="h-12 w-12 text-gray-400" />
                                    </div>

                                    <div class="flex justify-between">
                                        <button v-if="!lesson.completed" @click="completeLesson(lesson)"
                                            class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                                            Marcar como Concluída
                                        </button>
                                        <button v-else
                                            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md cursor-not-allowed">
                                            Lição Concluída
                                        </button>

                                        <button v-if="index < selectedCourse.lessons.length - 1 && lesson.completed"
                                            @click="goToNextLesson(index)"
                                            class="px-4 py-2 bg-emerald-100 text-emerald-700 rounded-md hover:bg-emerald-200 transition-colors">
                                            Próxima Lição
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- User Profile Page - NEW -->
            <div v-else-if="currentPage === 'profile'" class="space-y-6">
                <h1 class="text-3xl font-bold text-emerald-800 mb-6">Seu Perfil</h1>

                <!-- Login required message -->
                <div v-if="!isLoggedIn" class="bg-amber-50 border border-amber-200 rounded-lg p-6 text-center">
                    <lock-icon class="h-12 w-12 text-amber-500 mx-auto mb-4" />
                    <h2 class="text-xl font-semibold mb-2">Acesso Restrito</h2>
                    <p class="text-gray-600 mb-4">Faça login para acessar seu perfil.</p>
                    <button @click="showLoginModal = true"
                        class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                        Entrar
                    </button>
                </div>

                <!-- Profile content for logged in users -->
                <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="md:col-span-1">
                        <div class="bg-white rounded-lg shadow-md p-6">
                            <div class="flex flex-col items-center">
                                <div
                                    class="w-32 h-32 bg-emerald-100 rounded-full flex items-center justify-center mb-4">
                                    <user-icon class="h-16 w-16 text-emerald-600" />
                                </div>
                                <h2 class="text-xl font-semibold">{{ userProfile.name }}</h2>
                                <p class="text-gray-500">{{ userType === 'student' ? 'Estudante' : 'Voluntário' }}</p>

                                <div class="w-full mt-6 space-y-2">
                                    <button
                                        class="w-full py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                                        Editar Perfil
                                    </button>
                                    <button
                                        class="w-full py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">
                                        Alterar Senha
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="md:col-span-2">
                        <div class="bg-white rounded-lg shadow-md p-6">
                            <h3 class="text-lg font-semibold mb-4">Informações Pessoais</h3>

                            <div class="space-y-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Nome Completo</label>
                                    <input type="text" v-model="userProfile.name"
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md" />
                                </div>

                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                                    <input type="email" v-model="userProfile.email"
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md" />
                                </div>

                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Celular</label>
                                    <input type="tel" v-model="userProfile.phone"
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md" />
                                </div>

                                <div v-if="userType === 'volunteer'">
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Tipo</label>
                                    <select class="w-full px-3 py-2 border border-gray-300 rounded-md">
                                        <option>ONG</option>
                                        <option>Professor Voluntário</option>
                                    </select>
                                </div>

                                <div v-if="userType === 'volunteer'">
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
                                    <textarea v-model="userProfile.description" rows="3"
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md"></textarea>
                                </div>

                                <div class="pt-4">
                                    <button
                                        class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                                        Salvar Alterações
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div v-if="userType === 'student'" class="bg-white rounded-lg shadow-md p-6 mt-6">
                            <h3 class="text-lg font-semibold mb-4">Meu Progresso</h3>

                            <div class="space-y-4">
                                <div v-for="(course, index) in enrolledCourses" :key="index"
                                    class="border-b pb-4 last:border-b-0">
                                    <div class="flex justify-between items-center mb-2">
                                        <h4 class="font-medium">{{ course.title }}</h4>
                                        <span class="text-sm text-gray-500">{{ course.progress }}% concluído</span>
                                    </div>
                                    <div class="w-full bg-gray-200 rounded-full h-2.5">
                                        <div class="bg-emerald-600 h-2.5 rounded-full"
                                            :style="{ width: course.progress + '%' }"></div>
                                    </div>
                                    <div class="mt-2 flex justify-end">
                                        <button @click="currentPage = 'course-detail'; selectedCourse = course"
                                            class="text-sm text-emerald-600 hover:text-emerald-500">
                                            Continuar →
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Instrument Schedule Page - NEW -->
            <div v-else-if="currentPage === 'instrument-schedule'" class="space-y-6">
                <div class="flex items-center mb-6">
                    <button @click="currentPage = 'instruments'" class="mr-4 p-2 rounded-full hover:bg-gray-100">
                        <arrow-left-icon class="h-5 w-5" />
                    </button>
                    <h1 class="text-3xl font-bold text-emerald-800">Disponibilidade do Instrumento</h1>
                </div>

                <div class="bg-white rounded-lg shadow-md overflow-hidden">
                    <div class="p-6">
                        <div class="flex items-center mb-6">
                            <div class="bg-emerald-100 p-3 rounded-md mr-4">
                                <component :is="selectedInstrument.icon" class="h-10 w-10 text-emerald-600" />
                            </div>
                            <div>
                                <h2 class="text-xl font-semibold">{{ selectedInstrument.name }}</h2>
                                <p class="text-gray-500">{{ selectedInstrument.description }}</p>
                                <span
                                    class="inline-block mt-1 px-2 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs">
                                    Disponibilizado por: {{ selectedInstrument.source }}
                                </span>
                            </div>
                        </div>

                        <div class="mb-6">
                            <h3 class="text-lg font-semibold mb-3">Horários Disponíveis</h3>

                            <div class="grid grid-cols-7 gap-2 mb-4">
                                <div v-for="(day, index) in ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']"
                                    :key="index" class="text-center font-medium text-sm">
                                    {{ day }}
                                </div>

                                <div v-for="i in 7" :key="i"
                                    class="aspect-square border rounded-md flex items-center justify-center cursor-pointer hover:bg-gray-50"
                                    :class="{ 'bg-emerald-50 border-emerald-300': selectedDay === i }"
                                    @click="selectedDay = i">
                                    {{ i + 14 }}
                                </div>
                            </div>

                            <div v-if="selectedDay !== null" class="border rounded-md p-4">
                                <h4 class="font-medium mb-3">Horários para {{ ['Domingo', 'Segunda', 'Terça', 'Quarta',
                                    'Quinta', 'Sexta', 'Sábado'][selectedDay % 7] }}</h4>

                                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
                                    <button v-for="(slot, index) in availableTimeSlots" :key="index"
                                        class="py-2 px-3 border rounded-md text-center text-sm"
                                        :class="{ 'bg-emerald-100 border-emerald-300 text-emerald-800': selectedTimeSlot === index }"
                                        @click="selectedTimeSlot = index">
                                        {{ slot }}
                                    </button>
                                </div>

                                <div class="mt-4 flex justify-end">
                                    <button :disabled="selectedTimeSlot === null"
                                        :class="{ 'bg-emerald-600 hover:bg-emerald-500': selectedTimeSlot !== null, 'bg-gray-300 cursor-not-allowed': selectedTimeSlot === null }"
                                        class="px-4 py-2 text-white rounded-md transition-colors">
                                        Reservar Horário
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Manage Instruments Page (for volunteers) - NEW -->
            <div v-else-if="currentPage === 'manage-instruments'" class="space-y-6">
                <h1 class="text-3xl font-bold text-emerald-800 mb-6">Gerenciar Instrumentos</h1>

                <!-- Login required message -->
                <div v-if="!isLoggedIn || userType !== 'volunteer'"
                    class="bg-amber-50 border border-amber-200 rounded-lg p-6 text-center">
                    <lock-icon class="h-12 w-12 text-amber-500 mx-auto mb-4" />
                    <h2 class="text-xl font-semibold mb-2">Acesso Restrito</h2>
                    <p class="text-gray-600 mb-4">Esta área é exclusiva para ONGs e professores voluntários.</p>
                    <button @click="showLoginModal = true"
                        class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                        Entrar como Voluntário
                    </button>
                </div>

                <!-- Instrument management for volunteers -->
                <div v-else>
                    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
                        <div class="flex justify-between items-center mb-4">
                            <h2 class="text-xl font-semibold">Seus Instrumentos Disponibilizados</h2>
                            <button @click="showAddInstrumentModal = true"
                                class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                                Adicionar Instrumento
                            </button>
                        </div>

                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Instrumento
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Status
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Reservas
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Ações
                                        </th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
                                    <tr v-for="(instrument, index) in volunteerInstruments" :key="index">
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <div class="flex items-center">
                                                <div class="bg-emerald-100 p-2 rounded-md mr-3">
                                                    <component :is="instrument.icon" class="h-5 w-5 text-emerald-600" />
                                                </div>
                                                <div>
                                                    <div class="font-medium">{{ instrument.name }}</div>
                                                    <div class="text-sm text-gray-500">{{ instrument.description }}
                                                    </div>
                                                </div>
                                            </div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <span class="px-2 py-1 text-xs rounded-full"
                                                :class="instrument.available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                                                {{ instrument.available ? 'Disponível' : 'Indisponível' }}
                                            </span>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {{ instrument.bookings }} reservas
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm">
                                            <button class="text-emerald-600 hover:text-emerald-500 mr-3">Editar</button>
                                            <button class="text-red-600 hover:text-red-500">Remover</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Manage Schedule Page (for volunteers) - NEW -->
            <div v-else-if="currentPage === 'manage-schedule'" class="space-y-6">
                <h1 class="text-3xl font-bold text-emerald-800 mb-6">Gerenciar Agenda</h1>

                <!-- Login required message -->
                <div v-if="!isLoggedIn || userType !== 'volunteer'"
                    class="bg-amber-50 border border-amber-200 rounded-lg p-6 text-center">
                    <lock-icon class="h-12 w-12 text-amber-500 mx-auto mb-4" />
                    <h2 class="text-xl font-semibold mb-2">Acesso Restrito</h2>
                    <p class="text-gray-600 mb-4">Esta área é exclusiva para ONGs e professores voluntários.</p>
                    <button @click="showLoginModal = true"
                        class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                        Entrar como Voluntário
                    </button>
                </div>

                <!-- Schedule management for volunteers -->
                <div v-else>
                    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
                        <div class="flex justify-between items-center mb-4">
                            <h2 class="text-xl font-semibold">Sua Disponibilidade</h2>
                            <button
                                class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                                Adicionar Horário
                            </button>
                        </div>

                        <div class="grid grid-cols-7 gap-2 mb-6">
                            <div v-for="(day, index) in ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']" :key="index"
                                class="text-center font-medium text-sm">
                                {{ day }}
                            </div>

                            <div v-for="i in 7" :key="i"
                                class="aspect-square border rounded-md flex items-center justify-center cursor-pointer hover:bg-gray-50"
                                :class="{ 'bg-emerald-50 border-emerald-300': selectedScheduleDay === i }"
                                @click="selectedScheduleDay = i">
                                {{ i + 14 }}
                            </div>
                        </div>

                        <div v-if="selectedScheduleDay !== null" class="border rounded-md p-4">
                            <h3 class="font-medium mb-3">Horários para {{ ['Domingo', 'Segunda', 'Terça', 'Quarta',
                                'Quinta', 'Sexta', 'Sábado'][selectedScheduleDay % 7] }}</h3>

                            <div class="space-y-3">
                                <div v-for="(slot, index) in volunteerSchedule" :key="index"
                                    class="flex items-center justify-between p-3 border rounded-md">
                                    <div>
                                        <span class="font-medium">{{ slot.time }}</span>
                                        <span class="text-sm text-gray-500 ml-2">{{ slot.instrument }}</span>
                                    </div>
                                    <div class="flex items-center">
                                        <span class="px-2 py-1 text-xs rounded-full mr-3"
                                            :class="slot.booked ? 'bg-amber-100 text-amber-800' : 'bg-green-100 text-green-800'">
                                            {{ slot.booked ? 'Reservado' : 'Disponível' }}
                                        </span>
                                        <button class="text-red-600 hover:text-red-500">
                                            <x-icon class="h-5 w-5" />
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div class="mt-4 flex justify-between">
                                <button
                                    class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">
                                    Definir Indisponibilidade
                                </button>
                                <button
                                    class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                                    Adicionar Horário
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="bg-white rounded-lg shadow-md p-6">
                        <h2 class="text-xl font-semibold mb-4">Próximas Reservas</h2>

                        <div class="space-y-4">
                            <div v-for="(booking, index) in upcomingBookings" :key="index"
                                class="border rounded-md p-4">
                                <div class="flex justify-between">
                                    <div>
                                        <h3 class="font-medium">{{ booking.student }}</h3>
                                        <p class="text-sm text-gray-500">{{ booking.instrument }}</p>
                                    </div>
                                    <div class="text-right">
                                        <p class="font-medium">{{ booking.date }}</p>
                                        <p class="text-sm text-gray-500">{{ booking.time }}</p>
                                    </div>
                                </div>
                                <div class="flex justify-end mt-3">
                                    <button class="text-red-600 hover:text-red-500 mr-3">Cancelar</button>
                                    <button class="text-emerald-600 hover:text-emerald-500">Confirmar</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <!-- Add Instrument Modal (for volunteers) -->
        <div v-if="showAddInstrumentModal"
            class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-6 w-full max-w-md">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-xl font-bold">Adicionar Instrumento</h2>
                    <button @click="showAddInstrumentModal = false" class="text-gray-500 hover:text-gray-700">
                        <x-icon class="h-5 w-5" />
                    </button>
                </div>

                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Instrumento</label>
                        <input type="text" class="w-full px-3 py-2 border border-gray-300 rounded-md"
                            placeholder="Ex: Violão Clássico" />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
                        <textarea class="w-full px-3 py-2 border border-gray-300 rounded-md"
                            placeholder="Descreva o instrumento, condições, etc." rows="3"></textarea>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Instrumento</label>
                        <select class="w-full px-3 py-2 border border-gray-300 rounded-md">
                            <option>Cordas</option>
                            <option>Percussão</option>
                            <option>Sopro</option>
                            <option>Teclas</option>
                            <option>Outro</option>
                        </select>
                    </div>
                    <div class="flex items-center">
                        <input type="checkbox" id="available" class="h-4 w-4 text-emerald-600 border-gray-300 rounded"
                            checked />
                        <label for="available" class="ml-2 block text-sm text-gray-700">
                            Disponível para uso
                        </label>
                    </div>
                    <div class="flex justify-end">
                        <button @click="showAddInstrumentModal = false"
                            class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors mr-2">
                            Cancelar
                        </button>
                        <button @click="showAddInstrumentModal = false"
                            class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                            Adicionar
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="bg-gray-800 text-white py-8">
            <div class="container mx-auto px-4">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div>
                        <h3 class="text-lg font-semibold mb-4">MusicaMaster</h3>
                        <p class="text-gray-400">Sua jornada musical começa aqui. Aprenda, pratique e evolua com nossos
                            recursos exclusivos.</p>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold mb-4">Links Rápidos</h3>
                        <ul class="space-y-2">
                            <li v-for="(item, index) in navItems" :key="index">
                                <a @click="currentPage = item.route"
                                    class="text-gray-400 hover:text-white cursor-pointer">{{ item.name }}</a>
                            </li>
                        </ul>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold mb-4">Contato</h3>
                        <p class="text-gray-400 mb-2">contato@musicamaster.com</p>
                        <p class="text-gray-400">+55 (11) 9999-9999</p>
                        <div class="flex space-x-4 mt-4">
                            <a href="#" class="text-gray-400 hover:text-white">
                                <facebook-icon class="h-5 w-5" />
                            </a>
                            <a href="#" class="text-gray-400 hover:text-white">
                                <instagram-icon class="h-5 w-5" />
                            </a>
                            <a href="#" class="text-gray-400 hover:text-white">
                                <youtube-icon class="h-5 w-5" />
                            </a>
                        </div>
                    </div>
                </div>
                <div class="border-t border-gray-700 mt-8 pt-6 text-center text-gray-400">
                    <p>&copy; {{ new Date().getFullYear() }} MusicaMaster. Todos os direitos reservados.</p>
                </div>
            </div>
        </footer>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import {
    Music as MusicIcon,
    Menu as MenuIcon,
    X as XIcon,
    BookOpen as BookOpenIcon,
    GraduationCap as GraduationCapIcon,
    Lock as LockIcon,
    Clock as ClockIcon,
    Users as UsersIcon,
    Facebook as FacebookIcon,
    Instagram as InstagramIcon,
    Youtube as YoutubeIcon,
    Guitar as GuitarIcon,
    Piano as PianoIcon,
    Mic as MicIcon,
    Drum as DrumIcon,
    FileText as FileTextIcon,
    Video as VideoIcon,
    Headphones as HeadphonesIcon,
    User as UserIcon,
    Check as CheckIcon,
    ChevronDown as ChevronDownIcon,
    Play as PlayIcon,
    ArrowLeft as ArrowLeftIcon
} from 'lucide-vue-next';

// State
const currentPage = ref('home');
const mobileMenuOpen = ref(false);
const isLoggedIn = ref(false);
const instrumentFilter = ref('Todos');
const userMenuOpen = ref(false);
const showLoginModal = ref(false);
const showAddInstrumentModal = ref(false);
const loginEmail = ref('');
const loginPassword = ref('');
const isVolunteerLogin = ref(false);
const userType = ref('student'); // 'student' or 'volunteer'
const selectedDay = ref(null);
const selectedTimeSlot = ref(null);
const selectedScheduleDay = ref(null);
const selectedCourse = ref(null);
const selectedInstrument = ref(null);

// User profile
const userProfile = ref({
    name: 'João Silva',
    email: 'joao.silva@email.com',
    phone: '(11) 98765-4321',
    description: 'Professor de música com 10 anos de experiência.'
});

// Navigation items
const navItems = [
    { name: 'Início', route: 'home' },
    { name: 'Artigos', route: 'articles' },
    { name: 'Instrumentos', route: 'instruments' },
    { name: 'Cursos', route: 'courses' }
];

// Recent updates for home page
const recentUpdates = [
    {
        title: 'Novo Curso de Violão',
        description: 'Aprenda os fundamentos do violão em nosso novo curso para iniciantes.',
        date: '2 dias atrás',
        icon: GuitarIcon
    },
    {
        title: 'Artigo: Teoria Musical Básica',
        description: 'Um guia completo sobre os fundamentos da teoria musical para iniciantes.',
        date: '5 dias atrás',
        icon: FileTextIcon
    },
    {
        title: 'Parceria com ONGs',
        description: 'Agora temos mais instrumentos disponíveis através de nossas parcerias com ONGs.',
        date: '1 semana atrás',
        icon: MusicIcon
    }
];

// Articles data
const articles = [
    {
        title: 'Como Escolher Seu Primeiro Instrumento',
        excerpt: 'Um guia completo para ajudar iniciantes a escolher o instrumento ideal para começar sua jornada musical.',
        category: 'Guia',
        date: '15 de Maio, 2023',
        icon: MusicIcon
    },
    {
        title: 'Fundamentos da Teoria Musical',
        excerpt: 'Entenda os conceitos básicos da teoria musical que todo músico iniciante deve conhecer.',
        category: 'Teoria',
        date: '10 de Maio, 2023',
        icon: FileTextIcon
    },
    {
        title: 'Técnicas de Prática Eficiente',
        excerpt: 'Aprenda como maximizar seu tempo de prática e evoluir mais rapidamente em seu instrumento.',
        category: 'Prática',
        date: '5 de Maio, 2023',
        icon: HeadphonesIcon
    },
    {
        title: 'História do Jazz',
        excerpt: 'Uma jornada pela história do jazz e como ele influenciou a música moderna.',
        category: 'História',
        date: '1 de Maio, 2023',
        icon: VideoIcon
    }
];

// My instruments
const myInstruments = [
    {
        name: 'Violão Acústico',
        addedDate: '10/04/2023',
        icon: GuitarIcon
    }
];

// Available instruments
const availableInstruments = [
    {
        name: 'Violão Clássico',
        description: 'Violão para iniciantes em bom estado.',
        source: 'ONGs',
        icon: GuitarIcon
    },
    {
        name: 'Piano Digital',
        description: 'Piano digital com 88 teclas, ideal para estudantes.',
        source: 'Professores',
        icon: PianoIcon
    },
    {
        name: 'Flauta Doce',
        description: 'Flauta doce soprano, perfeita para iniciantes.',
        source: 'ONGs',
        icon: MusicIcon
    },
    {
        name: 'Ukulele',
        description: 'Ukulele soprano em ótimo estado.',
        source: 'Professores',
        icon: GuitarIcon
    },
    {
        name: 'Bateria Eletrônica',
        description: 'Bateria eletrônica para prática silenciosa.',
        source: 'Professores',
        icon: DrumIcon
    },
    {
        name: 'Microfone',
        description: 'Microfone dinâmico para aulas de canto.',
        source: 'ONGs',
        icon: MicIcon
    }
];

// Filtered instruments based on selection
const filteredAvailableInstruments = computed(() => {
    if (instrumentFilter.value === 'Todos') {
        return availableInstruments;
    }
    return availableInstruments.filter(instrument => instrument.source === instrumentFilter.value);
});

// Courses data with lessons
const courses = [
    {
        title: 'Violão para Iniciantes',
        description: 'Aprenda os acordes básicos e comece a tocar suas músicas favoritas.',
        level: 'Iniciante',
        duration: '4 semanas',
        students: 1245,
        icon: GuitarIcon,
        enrolled: true,
        progress: 65,
        lessons: [
            {
                title: 'Introdução ao Violão',
                duration: '15 min',
                description: 'Conheça as partes do violão e aprenda a postura correta para tocar.',
                completed: true,
                expanded: false,
                video: true
            },
            {
                title: 'Primeiros Acordes',
                duration: '20 min',
                description: 'Aprenda os acordes básicos: Dó (C), Sol (G) e Ré (D).',
                completed: true,
                expanded: false,
                video: true
            },
            {
                title: 'Ritmos Básicos',
                duration: '25 min',
                description: 'Pratique ritmos simples para acompanhar músicas populares.',
                completed: false,
                expanded: false,
                video: true
            },
            {
                title: 'Sua Primeira Música',
                duration: '30 min',
                description: 'Aprenda a tocar uma música completa usando os acordes e ritmos aprendidos.',
                completed: false,
                expanded: false,
                video: true
            }
        ]
    },
    {
        title: 'Fundamentos do Piano',
        description: 'Domine as técnicas básicas do piano e leitura de partituras.',
        level: 'Iniciante',
        duration: '6 semanas',
        students: 890,
        icon: PianoIcon,
        enrolled: true,
        progress: 30,
        lessons: []
    },
    {
        title: 'Introdução à Bateria',
        description: 'Aprenda ritmos básicos e técnicas de coordenação na bateria.',
        level: 'Iniciante',
        duration: '5 semanas',
        students: 723,
        icon: DrumIcon,
        enrolled: false,
        progress: 0,
        lessons: []
    },
    {
        title: 'Canto para Iniciantes',
        description: 'Desenvolva sua voz e aprenda técnicas vocais fundamentais.',
        level: 'Iniciante',
        duration: '8 semanas',
        students: 1056,
        icon: MicIcon,
        enrolled: false,
        progress: 0,
        lessons: []
    }
];

// Enrolled courses for profile page
const enrolledCourses = computed(() => {
    return courses.filter(course => course.enrolled);
});

// Available time slots for instrument booking
const availableTimeSlots = [
    '09:00 - 10:00',
    '10:00 - 11:00',
    '11:00 - 12:00',
    '14:00 - 15:00',
    '15:00 - 16:00',
    '16:00 - 17:00',
    '17:00 - 18:00'
];

// Volunteer instruments
const volunteerInstruments = [
    {
        name: 'Violão Clássico',
        description: 'Violão para iniciantes em bom estado.',
        icon: GuitarIcon,
        available: true,
        bookings: 5
    },
    {
        name: 'Flauta Doce',
        description: 'Flauta doce soprano, perfeita para iniciantes.',
        icon: MusicIcon,
        available: true,
        bookings: 2
    },
    {
        name: 'Ukulele',
        description: 'Ukulele soprano em ótimo estado.',
        icon: GuitarIcon,
        available: false,
        bookings: 0
    }
];

// Volunteer schedule
const volunteerSchedule = [
    {
        time: '09:00 - 10:00',
        instrument: 'Violão Clássico',
        booked: true
    },
    {
        time: '10:00 - 11:00',
        instrument: 'Violão Clássico',
        booked: false
    },
    {
        time: '14:00 - 15:00',
        instrument: 'Flauta Doce',
        booked: false
    },
    {
        time: '15:00 - 16:00',
        instrument: 'Ukulele',
        booked: true
    }
];

// Upcoming bookings
const upcomingBookings = [
    {
        student: 'Maria Santos',
        instrument: 'Violão Clássico',
        date: '18/05/2023',
        time: '09:00 - 10:00'
    },
    {
        student: 'Pedro Oliveira',
        instrument: 'Ukulele',
        date: '19/05/2023',
        time: '15:00 - 16:00'
    }
];

// Methods
const login = () => {
    isLoggedIn.value = true;
    userType.value = isVolunteerLogin.value ? 'volunteer' : 'student';
    showLoginModal.value = false;
};

const completeLesson = (lesson) => {
    lesson.completed = true;

    // Update course progress
    if (selectedCourse.value) {
        const totalLessons = selectedCourse.value.lessons.length;
        const completedLessons = selectedCourse.value.lessons.filter(l => l.completed).length;
        selectedCourse.value.progress = Math.round((completedLessons / totalLessons) * 100);
    }
};

const goToNextLesson = (currentIndex) => {
    // Close current lesson
    selectedCourse.value.lessons[currentIndex].expanded = false;

    // Open next lesson
    if (currentIndex < selectedCourse.value.lessons.length - 1) {
        selectedCourse.value.lessons[currentIndex + 1].expanded = true;
    }
};
</script>

<style>
/* Estilos adicionais podem ser adicionados aqui se necessário */
</style>