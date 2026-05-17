import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../lib/api";
import Marquee from "../components/Marquee";
import { ArrowUpRight, Compass, Network, BookOpen } from "lucide-react";

export default function Home() {
  const [data, setData] = useState(null);
  useEffect(() => { api.get("/explore/portal").then((r) => setData(r.data)); }, []);
  const d = data || {};

  return (
    <div>
      {/* HERO */}
      <section className="relative max-w-[1480px] mx-auto px-6 pt-14 pb-10">
        <div className="grid lg:grid-cols-12 gap-6">
          <div className="lg:col-span-8">
            <div className="meta-ink mb-5" data-testid="hero-tagline">vol. i / no. 001 · the slow internet for music</div>
            <h1 className="font-display font-black tracking-tighter leading-[0.88] text-[clamp(3rem,8.4vw,8.4rem)]">
              music<br/>
              <span className="italic font-editorial font-normal text-[var(--hyperpop)]">culture</span><br/>
              is a place.
            </h1>
            <p className="font-editorial text-2xl md:text-3xl italic mt-7 max-w-xl leading-snug">
              not a stream to consume. a world to <span className="bg-[var(--acid)] px-1">inhabit</span>.
              build the lore. argue the theories. follow the samples home.
            </p>
            <div className="flex flex-wrap gap-3 mt-8">
              <Link to="/explore" className="brutal-btn" data-testid="hero-cta-explore"><Compass size={16}/>enter the archive</Link>
              <Link to="/connections" className="brutal-btn acid" data-testid="hero-cta-map"><Network size={16}/>open the map</Link>
            </div>
          </div>
          <aside className="lg:col-span-4">
            <div className="brutal-card-static p-6 relative overflow-hidden grain" data-testid="manifesto-card">
              <div className="meta-ink mb-3">manifesto · 001</div>
              <p className="font-editorial text-xl leading-snug">
                we believe the most interesting place in music is <em>between</em> the songs. the producer credits. the sample chain. the line you didn't notice until your fourteenth listen. the friend who put you on.
              </p>
              <p className="font-editorial text-xl leading-snug mt-4">
                we are building a home for that <em>between</em>.
              </p>
            </div>
            <div className="mt-6 grid grid-cols-2 gap-3">
              <div className="brutal-card-static p-4"><div className="meta-ink">scenes</div><div className="font-display font-black text-3xl mt-1">9</div></div>
              <div className="brutal-card-static p-4 bg-[var(--hyperpop)] text-white"><div className="meta-ink !text-white/80">lore entries</div><div className="font-display font-black text-3xl mt-1">{(d.rabbit_holes || []).length * 27 + 142}</div></div>
              <div className="brutal-card-static p-4"><div className="meta-ink">curators</div><div className="font-display font-black text-3xl mt-1">{(d.contributors || []).length}+</div></div>
            </div>
          </aside>
        </div>
      </section>

      <Marquee items={["BLOND / BLONDE — same record, two selves", "the poem is the album", "the mask is not a costume", "in rainbows is the only staying record", "click here for the rabbit hole", "your taste deserves a footnote"]} />

      {/* RABBIT HOLES */}
      <section className="max-w-[1480px] mx-auto px-6 mt-16">
        <div className="flex items-end justify-between mb-6">
          <div>
            <div className="meta-ink mb-2">today's rabbit holes</div>
            <h2 className="font-display font-black text-4xl md:text-5xl tracking-tighter">five questions worth losing the afternoon to.</h2>
          </div>
          <Link to="/lore" className="brutal-btn invert hidden md:inline-flex" data-testid="see-all-lore">all lore <ArrowUpRight size={14}/></Link>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {(d.rabbit_holes || []).map((l, i) => (
            <Link key={l.id} to={`/lore/${l.id}`} className="brutal-card p-6 block group" data-testid={`rabbit-hole-${l.id}`}>
              <div className="meta-ink mb-3">entry · {String(i+1).padStart(3,'0')}</div>
              <h3 className="font-display font-bold text-xl tracking-tight leading-tight">{l.title}</h3>
              <p className="font-editorial italic text-lg mt-3 line-clamp-3">{l.excerpt}</p>
              <div className="mt-5 flex items-center justify-between">
                <span className="meta-ink">by {l.author}</span>
                <span className="tag-chip">{l.depth} · {l.votes}↑</span>
              </div>
            </Link>
          ))}
        </div>
      </section>
      {/* FEATURED ALBUM */}
      {d.featured_album && (
        <section className="max-w-[1480px] mx-auto px-6 mt-20">
          <div className="meta-ink mb-2">universe of the week</div>
          <Link to={`/album/${d.featured_album.id}`} className="brutal-card p-10 block dark-universe grain relative overflow-hidden" data-testid="featured-album">
            <div className="grid lg:grid-cols-2 gap-8 items-center relative z-10">
              <div>
                <div className="meta">{d.featured_album.year} · album as universe</div>
                <h2 className="font-display font-black text-6xl md:text-7xl tracking-tighter mt-3">{d.featured_album.title}</h2>
                <p className="font-editorial italic text-2xl mt-4">{d.featured_album.universe_tagline}</p>
                <div className="flex flex-wrap gap-2 mt-6">
                  {(d.featured_album.motifs || []).map((m) => <span key={m} className="tag-chip">{m}</span>)}
                </div>
              </div>
              <div className="aspect-square w-full max-w-md ml-auto relative" style={{ background: d.featured_album.color }}>
                <div className="absolute inset-0 grain" />
                <div className="absolute inset-6 border-2 border-[var(--ink)] flex flex-col justify-between p-6">
                  <span className="meta-ink">side a / side b</span>
                  <span className="font-display font-black text-4xl tracking-tighter text-[var(--ink)] mix-blend-multiply">{d.featured_album.title.toLowerCase()}</span>
                </div>
              </div>
            </div>
          </Link>
        </section>
      )}

      {/* THEORIES */}
      <section className="max-w-[1480px] mx-auto px-6 mt-20">
        <div className="meta-ink mb-2">contested terrain</div>
        <h2 className="font-display font-black text-4xl md:text-5xl tracking-tighter mb-6">theories with citations.</h2>
        <div className="grid md:grid-cols-3 gap-5">
          {(d.theories || []).map((t) => (
            <Link key={t.id} to={`/theory/${t.id}`} className="brutal-card p-6" data-testid={`theory-${t.id}`}>
              <div className="meta-ink mb-3 flex items-center gap-2"><BookOpen size={12}/>{t.stance}</div>
              <h3 className="font-display font-bold text-xl tracking-tight">{t.title}</h3>
              <p className="font-editorial italic text-base mt-3 line-clamp-3">{t.abstract}</p>
              <div className="flex gap-2 mt-4">
                <span className="tag-chip">{t.supporters} co-sign</span>
                <span className="tag-chip" style={{background: 'var(--parchment-deep)'}}>{t.challengers} push back</span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* CONTRIBUTORS */}
      <section className="max-w-[1480px] mx-auto px-6 mt-20">
        <div className="meta-ink mb-2">the keepers</div>
        <h2 className="font-display font-black text-4xl md:text-5xl tracking-tighter mb-6">curators worth following down a hole.</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-5">
          {(d.contributors || []).map((c) => (
            <Link key={c.handle} to={`/c/${c.handle}`} className="brutal-card p-5" data-testid={`contributor-${c.handle}`}>
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 border-2 border-[var(--ink)] bg-[var(--hyperpop)] flex items-center justify-center font-display font-black text-xl">{c.name[0]?.toUpperCase()}</div>
                <div>
                  <div className="font-display font-bold">@{c.handle}</div>
                  <div className="meta-ink">depth {c.depth_score}</div>
                </div>
              </div>
              <p className="font-editorial italic mt-3 text-base line-clamp-2">{c.bio}</p>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
