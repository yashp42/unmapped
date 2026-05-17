export default function Footer() {
  return (
    <footer className="mt-24 border-t-2 border-[var(--ink)] py-12 px-6" data-testid="site-footer">
      <div className="max-w-[1480px] mx-auto grid md:grid-cols-3 gap-10">
        <div>
          <div className="font-display font-black text-3xl tracking-tighter">unmapped</div>
          <p className="font-editorial text-lg mt-2 italic">music culture is a place to inhabit, not a stream to consume.</p>
        </div>
        <div>
          <div className="meta-ink mb-3">the principles</div>
          <ul className="font-display text-sm space-y-1">
            <li>· anti-feed</li><li>· earned complexity</li><li>· productive friction</li>
            <li>· ambient social</li><li>· progressive revelation</li>
          </ul>
        </div>
        <div>
          <div className="meta-ink mb-3">the archive</div>
          <p className="font-editorial italic">a slow, dense, deeply linked place. read carefully. contribute generously. argue politely.</p>
        </div>
      </div>
      <div className="max-w-[1480px] mx-auto mt-10 meta-ink">© unmapped · v0.1 · the rabbit hole begins here</div>
    </footer>
  );
}
