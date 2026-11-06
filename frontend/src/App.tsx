function App() {
  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4">
        <div className="flex items-center gap-3">
          <img
            src="/hireforce-logo.svg"
            alt="HireForce"
            className="h-10 w-auto"
          />
          <span className="text-xl font-bold">HireForce</span>
        </div>

        <span className="rounded-full bg-blue-50 px-4 py-2 text-sm font-medium text-blue-700">
          Organization Platform
        </span>
      </header>

      <section className="mx-auto flex min-h-[75vh] max-w-5xl flex-col items-center justify-center px-6 text-center">
        <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-blue-600">
          HireForce
        </p>

        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
          Organization Management
        </h1>

        <p className="mt-5 max-w-xl text-base leading-7 text-slate-600">
          The organization frontend foundation is ready.
          Authentication, company profiles, interview management
          and candidate evaluation modules will be integrated next.
        </p>
      </section>
    </main>
  );
}

export default App;
