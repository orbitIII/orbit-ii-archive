const DATA_FILES = {
  fundament: "/orbit_fundament.json",
  dna: "/orbit_kultur_dna.json",
  prinzipien: "/orbit_prinzipien_index.json",
  werk: "/orbit_werk_pour_cet_instant.json",
  mam: "/orbit_referenz_mam_paris.json",
  verflechtungen: "/orbit_verflechtungen.json",
  identitaet: "/orbit_identitaet.json",
};

export async function loadOrbitData() {
  const entries = await Promise.all(
    Object.entries(DATA_FILES).map(async ([key, path]) => {
      const res = await fetch(path);
      if (!res.ok) throw new Error(`${path}: HTTP ${res.status}`);
      return [key, await res.json()];
    })
  );
  return Object.fromEntries(entries);
}

export function buildState(data) {
  const principles = data.dna?.kunst_prinzipien?.principles ?? {};
  const combinations = data.dna?.kunst_prinzipien?.principle_combinations ?? {};
  const forbidden = data.dna?.core_dna?.mood_axes?.forbidden ?? [];
  const litmus = data.dna?.core_dna?.litmus_question ?? "";
  const fundament = data.fundament?.referenz_fundament ?? data.dna?.referenz_fundament;
  const schichten = data.fundament?.schichtenmodell ?? {};
  const matrix = data.fundament?.prinzipien_matrix?.matrix ?? {};
  const weaves = data.verflechtungen?.weaves ?? [];
  const mamMovements = data.mam?.kuenstler_nach_bewegung ?? {};
  const mamPrinciples = data.mam?.mam_prinzipien?.principles ?? {};
  const werkPrinciples = data.werk?.kunst_prinzipien?.aktiv ?? [];
  const phases = data.identitaet?.phasen ?? {};
  const pflicht = data.prinzipien?.pflicht_regel ?? {};

  const principleList = Object.entries(principles).map(([id, p]) => ({
    id,
    label: p.label ?? id,
    definition: p.definition ?? "",
    orbit_meaning: p.orbit_meaning ?? "",
    forbidden: p.forbidden ?? [],
    exemplars: p.exemplars ?? [],
  }));

  return {
    data,
    fundament,
    schichten,
    matrix,
    principles: principleList,
    combinations,
    forbidden,
    litmus,
    weaves,
    mamMovements,
    mamPrinciples,
    werk: data.werk,
    werkPrinciples,
    phases,
    pflicht,
    mission: data.dna?.mission ?? "",
    essence: data.dna?.core_dna?.essence ?? "",
    tension: data.dna?.core_dna?.tension_axis ?? {},
    bridges: data.fundament?.cross_saeule_bridges?.bridges ?? [],
  };
}
